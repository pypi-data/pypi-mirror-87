from enum import Enum
from collections import namedtuple
from typing import List
import random
from gpustat.core import GPUStatCollection


class GpuStatusMode(Enum):
    FAKE = 1
    GPU_STAT = 2


GpuState = namedtuple('GpuInfo', ['name', 'memMax', 'memNow', 'load'])

GpuInfo = List[GpuState]


class GpuStatus:
    def __init__(self, config: dict):
        if config['fake']:
            self.mode = GpuStatusMode.FAKE
            self.fake_gpu_name = config['gpu_name']
            self.fake_gpu_mem = config['gpu_mem']
            self.fake_gpu_count = config['gpu_num']
        else:
            self.mode = GpuStatusMode.GPU_STAT

    def _generate_fake_state(self):
        mem_load = random.random()
        load = random.random()
        return GpuState(self.fake_gpu_name, self.fake_gpu_mem, self.fake_gpu_mem * mem_load, load)

    def get_info_fake(self) -> GpuInfo:
        return [self._generate_fake_state() for _ in range(self.fake_gpu_count)]

    def get_info_gpustat(self) -> GpuInfo:
        stat = GPUStatCollection.new_query().jsonify()
        return [GpuState(name=obj['name'], memMax=obj['memory.total'] / 1e3, memNow=obj['memory.used'] / 1e3, load=obj['utilization.gpu'] / 100)
                for obj in stat['gpus']]

    def get_info(self) -> GpuInfo:
        if self.mode == GpuStatusMode.FAKE:
            return self.get_info_fake()
        else:
            return self.get_info_gpustat()
