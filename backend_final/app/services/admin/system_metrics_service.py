import psutil
import time

BOOT_TIME = time.time()


def get_system_metrics():
    cpu_usage = round(psutil.cpu_percent(interval=0.5), 2)
    memory_usage = round(psutil.virtual_memory().percent, 2)
    disk_usage = round(psutil.disk_usage("/").percent, 2)
    uptime_seconds = int(time.time() - BOOT_TIME)

    return {
        "cpu_usage_percent": cpu_usage,
        "memory_usage_percent": memory_usage,
        "disk_usage_percent": disk_usage,
        "backend_uptime_seconds": uptime_seconds,
    }
