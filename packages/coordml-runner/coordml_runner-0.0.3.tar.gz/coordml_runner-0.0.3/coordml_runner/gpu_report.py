import asyncio
from central_client.client import CentralClient
from gpu_status import GpuStatus, GpuStatusMode
import logging

logger = logging.getLogger(__name__)


class GpuReport:
    def __init__(self, client: CentralClient, gpu_status: GpuStatus):
        self.client = client
        self.gpu_status = gpu_status

    async def run(self):
        while True:
            await asyncio.sleep(1.0)
            info = self.gpu_status.get_info()
            await self.client.report_gpu(info)
            logger.info(f'reported gpu info to server: {info}')
