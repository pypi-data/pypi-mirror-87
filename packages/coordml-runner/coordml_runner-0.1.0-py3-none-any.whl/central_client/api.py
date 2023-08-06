import aiohttp
import asyncio
from gpu_status import *
from typing import Dict


class CentralAPI:
    def __init__(self, api_entry: str = 'http://127.0.0.1:8888/api'):
        self.api_entry = api_entry

    async def get(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

    async def post(self, url, data):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                resp = response
                return await resp.json()

    def url_of_api(self, *args):
        return self.api_entry + '/' + '/'.join(args)

    async def register(self, name: str) -> dict:
        return await self.post(self.url_of_api('workers', 'register'), {'name': name})

    async def report_gpu(self, worker_id: str, gpu_info: GpuInfo):
        payload = {
            'workerId': worker_id,
            'gpuStatus': [{
                'name': gpu.name,
                'memUsage': {
                    'used': gpu.memNow,
                    'capacity': gpu.memMax
                },
                'load': gpu.load
            } for gpu in gpu_info]
        }
        return await self.post(self.url_of_api('workers', 'reportGpu'), payload)

    async def worker_list(self):
        return await self.get(self.url_of_api('workers', 'list'))

    async def fetch_task(self, worker_id: str):
        url = self.url_of_api('workers', 'fetchTasks')
        url = f'{url}?workerId={worker_id}'
        return await self.get(url)

    async def report_result(self, worker_id: str, exp_id: str, graph_id: str, task_id: str, results: Dict[str, float]):
        url = self.url_of_api('workers', 'reportResult')
        url = f'{url}?workerId={worker_id}'
        payload = {
            'expId': exp_id,
            'graphId': graph_id,
            'taskId': task_id,
            'results': results
        }
        return await self.post(url, payload)
