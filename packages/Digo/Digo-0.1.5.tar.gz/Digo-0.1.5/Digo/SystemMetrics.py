import psutil
import nvgpu

from collections import OrderedDict
import json

def getSystemMetrics():

    systemMetrics = OrderedDict()
    systemMetrics["cpu_usage"] = psutil.cpu_percent()
    systemMetrics["memory_usage"] = psutil.virtual_memory().percent

    try : 
        systemMetrics["gpu_usage"] = round(nvgpu.gpu_info()[0]["mem_used_percent"],1)
    except FileNotFoundError:
        pass
    except Exception:
        pass

    return json.dumps(systemMetrics)