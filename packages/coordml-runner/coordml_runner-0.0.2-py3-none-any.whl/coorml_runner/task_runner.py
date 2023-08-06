import os.path as osp
from pathlib import Path
import logging
import parse
import asyncio
from central_client.client import CentralClient
from central_client.tasks import *
from gpu_status import GpuStatus
from typing import Dict
from enum import Enum

logger = logging.getLogger(__name__)

GraphMapping = Dict[str, RunnableGraph]
TaskIdentifier = Tuple[str, str]  # (graph_id, task_id)


class TaskStatus(Enum):
    DONE = 1
    READY = 2
    WAITING = 3


def preprocess_graph(task_graph: RunnableGraph) -> RunnableGraph:
    def f(x: RunnableTask) -> RunnableTask:
        x.task.status = TaskStatus.WAITING if x.task.status is None else TaskStatus.DONE
        return x

    return RunnableGraph(
        graph_id=task_graph.graph_id,
        dependencies=task_graph.dependencies,
        nodes=dict((x.task.task_id, f(x)) for x in task_graph.nodes)
    )


def extract_ready_nodes(task_graph: RunnableGraph) -> List[TaskIdentifier]:
    in_deg = {task_id: 0 for task_id in task_graph.nodes.keys()}
    for (first, then) in task_graph.dependencies:
        if task_graph.nodes[first].task.status != TaskStatus.DONE:
            in_deg[then] += 1
    ret = []
    for (key, task) in task_graph.nodes.items():
        if in_deg[key] == 0 and task.task.status == TaskStatus.WAITING:
            ret.append((task_graph.graph_id, key))
    return ret


class TaskRunner:
    def __init__(self, client: CentralClient, gpu_status: GpuStatus, log_path: str, runner_config: dict):
        self.client = client
        self.gpu_status = gpu_status
        self.log_path = osp.expanduser(log_path)

        self.max_tasks_per_gpu = runner_config['max_tasks_per_gpu']
        self.max_gpu_load = runner_config['max_gpu_load']
        self.min_gpu_mem = runner_config['min_gpu_mem']

        self.graphs: GraphMapping = dict()
        self.finish_queue = asyncio.Queue(maxsize=-1)
        self.ready_queue = asyncio.Queue(maxsize=-1)
        self.gpu_assignments: Dict[TaskIdentifier, int] = dict()

    async def run(self):
        while True:
            await asyncio.sleep(1.0)
            await self.handle_finished_tasks()
            await self.fetch_new_tasks()
            await self.add_ready_tasks()
            await self.dispatch_ready_tasks()

    async def fetch_new_tasks(self):
        tasks = await self.client.fetch_tasks()
        tasks = [preprocess_graph(graph) for graph in tasks]
        logger.info(f'Fetched new tasks from Central: {tasks}')
        for task in tasks:
            self.graphs[task.graph_id] = task

    async def add_ready_tasks(self):
        for graph in self.graphs.values():
            ready = extract_ready_nodes(graph)
            for graph_id, task_id in ready:
                self.graphs[graph_id].nodes[task_id].task.status = TaskStatus.READY
                await self.ready_queue.put((graph_id, task_id))
                logger.info(f'Put task into ready queue: {(graph_id, task_id)}')

    def get_available_gpus(self) -> List[int]:
        gpu_info = self.gpu_status.get_info()
        num_gpus = len(gpu_info)
        num_tasks = [0 for _ in range(num_gpus)]
        for (_, gpu_id) in self.gpu_assignments.items():
            if gpu_id >= num_gpus:
                logger.warning(f'Gpu number changed, there may be errors in the system')
            else:
                num_tasks[gpu_id] += 1
        ret = []
        for gpu_id in range(num_gpus):
            if num_tasks[gpu_id] < self.max_tasks_per_gpu and gpu_info[gpu_id].load < self.max_gpu_load and \
                    (gpu_info[gpu_id].memMax - gpu_info[gpu_id].memNow) > self.min_gpu_mem:
                ret.append(gpu_id)
        return ret

    def prepare_env(self, graph_id: str, task: RunnableTask, gpu_id: int):
        log_env_path = osp.join(self.log_path, 'graphs', graph_id, task.task.task_id)
        Path(log_env_path).mkdir(parents=True, exist_ok=True)
        arguments = [(key, val) for key, val in task.task.args.items()] + [('device', f'cuda:{gpu_id}')]
        cmd = f'python {task.task.executable} {" ".join(f"--{key} {val}" for key, val in arguments)}'
        log_path = osp.join(log_env_path, 'log')
        stderr_path = osp.join(log_env_path, 'stderr')
        script_path = osp.join(log_env_path, 'run.sh')

        cmd = f'{cmd} 2> {stderr_path} 1> {log_path}'
        cmd = f'cd {task.env_path}\n{cmd}'

        with open(script_path, 'w') as f:
            f.write(cmd)

        return log_env_path

    async def dispatch_ready_tasks(self):
        if self.ready_queue.empty():
            logger.info('Ready queue is empty, pass')
            return
        else:
            num_ready = self.ready_queue.qsize()
            gpu_available = self.get_available_gpus()
            num_dispatch = min(len(gpu_available), num_ready)
            logger.info(
                f'{num_ready} ready tasks, available Gpu: {gpu_available}, will dispatch {num_dispatch} task(s)')
            for i in range(num_dispatch):
                graph_id, task_id = self.ready_queue.get_nowait()
                gpu_id = gpu_available[i]
                self.gpu_assignments[(graph_id, task_id)] = gpu_id
                logger.info(f'Dispatch task: {(graph_id, task_id)} -> GPU {gpu_id}')
                asyncio.create_task(self.run_task(graph_id, task_id, gpu_id))

    def extract_task_result(self, log_env_path: str, graph_id: str, task_id: str) -> Dict[str, float]:
        runnable = self.graphs[graph_id].nodes[task_id]
        rule = parse.compile(runnable.result_parse)
        log_path = osp.join(log_env_path, 'log')

        with open(log_path, 'r') as f:
            lines = reversed(f.readlines())
            for line in lines:
                res = rule.parse(line)
                if res is not None:
                    return res.named

        return dict()

    async def run_task(self, graph_id: str, task_id: str, gpu_id: int):
        runnable = self.graphs[graph_id].nodes[task_id]
        log_env_path = self.prepare_env(graph_id, runnable, gpu_id)
        script_path = osp.join(log_env_path, 'run.sh')
        proc = await asyncio.create_subprocess_exec('sh', script_path, stdout=asyncio.subprocess.PIPE,
                                                    stderr=asyncio.subprocess.PIPE)
        logger.info(f'Task {(graph_id, task_id)} started with PID {proc.pid}, args {self.graphs[graph_id].nodes[task_id].task.args}')
        stdout, stderr = await proc.communicate()
        stdout = stdout.decode() if stdout else '[EMPTY]'
        stderr = stderr.decode() if stderr else '[EMPTY]'
        logger.info(f'Task {(graph_id, task_id)} finished with stdout {stdout} stderr {stderr}')

        # Try to extract log
        results = self.extract_task_result(log_env_path, graph_id, task_id)
        logger.info(f'Extracted task {(graph_id, task_id)} results {results}')

        # Report results to Central
        await self.client.report_result(graph_id, runnable, results)

        # Add task to finished queue
        await self.finish_queue.put((graph_id, task_id))

    async def handle_finished_tasks(self):
        while not self.finish_queue.empty():
            graph_id, task_id = self.finish_queue.get_nowait()

            # remove from gpu assignments
            self.gpu_assignments.pop((graph_id, task_id))

            # change task status
            self.graphs[graph_id].nodes[task_id].task.status = TaskStatus.DONE
