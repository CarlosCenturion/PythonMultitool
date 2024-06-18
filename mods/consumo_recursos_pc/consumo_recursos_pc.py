import psutil
import GPUtil
import time
import sys
from colorama import init, Fore, Style
from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetUtilizationRates, nvmlDeviceGetClockInfo, nvmlDeviceGetMemoryInfo, nvmlShutdown, NVML_CLOCK_GRAPHICS

# Initialize colorama
init(autoreset=True)

def get_network_usage():
    net_io = psutil.net_io_counters()
    return net_io.bytes_sent, net_io.bytes_recv

def get_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq()
    if cpu_freq:
        cpu_current = cpu_freq.current / 1000  # Convert to GHz
        cpu_max = cpu_freq.max / 1000  # Convert to GHz
    else:
        cpu_current = 0
        cpu_max = 0
    return cpu_percent, cpu_current, cpu_max

def get_ram_usage():
    mem = psutil.virtual_memory()
    return mem.percent, mem.used / (1024 ** 3), mem.total / (1024 ** 3)

def get_gpu_usage():
    try:
        nvmlInit()
        handle = nvmlDeviceGetHandleByIndex(0)
        utilization = nvmlDeviceGetUtilizationRates(handle)
        gpu_load = utilization.gpu  # GPU usage percentage
        gpu_mem_info = nvmlDeviceGetMemoryInfo(handle)
        gpu_used_mem = gpu_mem_info.used / (1024 ** 3)  # Used memory in GB
        gpu_total_mem = gpu_mem_info.total / (1024 ** 3)  # Total memory in GB
        nvmlShutdown()
        return gpu_load, gpu_used_mem, gpu_total_mem
    except Exception as e:
        return 0, 0, 0

def ejecutar():
    print("Monitoring system usage...")
    sent, recv = get_network_usage()
    while True:
        time.sleep(1)
        new_sent, new_recv = get_network_usage()
        sent_per_sec = (new_sent - sent) / 1024 / 1024  # Convert to MB
        recv_per_sec = (new_recv - recv) / 1024 / 1024  # Convert to MB

        cpu_usage_percent, cpu_current, cpu_max = get_cpu_usage()
        ram_usage_percent, ram_used, ram_total = get_ram_usage()
        gpu_usage_percent, gpu_used_mem, gpu_total_mem = get_gpu_usage()

        # Create the output string with colors
        output = (
            f"{Fore.GREEN}Sent: {sent_per_sec:.2f} MB/s{Style.RESET_ALL} | "
            f"{Fore.CYAN}Received: {recv_per_sec:.2f} MB/s{Style.RESET_ALL} | "
            f"{Fore.YELLOW}CPU: {cpu_usage_percent:.2f}% ({cpu_current:.2f}GHz){Style.RESET_ALL} | "
            f"{Fore.MAGENTA}RAM: {ram_usage_percent:.2f}% ({ram_used:.2f}GB/{ram_total:.2f}GB){Style.RESET_ALL} | "
            f"{Fore.BLUE}GPU: {gpu_usage_percent:.2f}% ({gpu_used_mem:.2f}GB/{gpu_total_mem:.2f}GB)"
        )

        # Print the output string, overwrite the previous line
        sys.stdout.write('\r' + output)
        sys.stdout.flush()

        sent, recv = new_sent, new_recv

if __name__ == "__main__":
    ejecutar()
