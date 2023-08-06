from collections import namedtuple
from typing import Tuple, List, Dict, Union


Dependency = Tuple[str, str]


class Task:
    def __init__(self, args: Dict[str, str], executable: str, meta: Dict[str, str], status, task_id: str):
        self.task_id = task_id
        self.executable = executable
        self.args = args
        self.meta = meta
        self.status = status


class RunnableTask:
    def __init__(self, exp_id: str, env_path: str, result_parse: str, task: Task):
        self.exp_id = exp_id
        self.env_path = env_path
        self.result_parse = result_parse
        self.task = task


class RunnableGraph:
    def __init__(self, graph_id: str, nodes: Union[List[RunnableTask], Dict[str, RunnableTask]], dependencies: List[Dependency]):
        self.graph_id = graph_id
        self.nodes = nodes
        self.dependencies = dependencies


def parse_task(obj: dict) -> Task:
    return Task(
        args=obj['args'],
        meta=obj['meta'],
        executable=obj['executable'],
        status=obj['status'],
        task_id=obj['taskId']
    )


def parse_dependencies(obj: List[dict]) -> List[Dependency]:
    return [(x[0], x[-1]) for x in obj]


def parse_runnable_task(obj: dict) -> RunnableTask:
    return RunnableTask(
        env_path=obj['envPath'],
        exp_id=obj['expId'],
        result_parse=obj['resultParse'],
        task=parse_task(obj['task'])
    )


def parse_runnable_graph(obj: dict) -> RunnableGraph:
    return RunnableGraph(
        graph_id=obj['graphId'],
        nodes=[parse_runnable_task(x) for x in obj['nodes']],
        dependencies=parse_dependencies(obj['dependencies'])
    )
