import asyncio
from gpu_status import GpuStatus, GpuStatusMode
from central_client.client import CentralClient
from coordml_runner.gpu_report import GpuReport
from coordml_runner.task_runner import TaskRunner


class Entry:
    def __init__(self, config):
        self.client = CentralClient(name=config['name'], api_endpoint=config['api_endpoint'])
        self.gpu_status = GpuStatus(config['gpu_mode'])
        self.gpu_report = GpuReport(client=self.client, gpu_status=self.gpu_status)
        self.task_runner = TaskRunner(client=self.client,
                                      gpu_status=self.gpu_status,
                                      log_path=config['log_path'],
                                      runner_config=config['runner'])

    async def start(self):
        await self.client.register()
        print(f'Runner registered, id {self.client.worker_id}')
        gpu_report_task = asyncio.create_task(self.gpu_report.run())
        print(f'GpuReport module spawned')
        task_runner = asyncio.create_task(self.task_runner.run())
        print(f'TaskRunner module spawned')
        print(f'Runner started')
        await asyncio.gather(gpu_report_task, task_runner)
