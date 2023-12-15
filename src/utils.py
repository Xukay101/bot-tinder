import psutil

def get_memory_usage():
    pid = psutil.Process()
    memory_info = pid.memory_info()
    return round(memory_info.rss / (1024 ** 2), 2)
