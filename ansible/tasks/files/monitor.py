from bcc import BPF
import os
import time
import psutil
import platform
from prometheus_client import start_http_server, Gauge
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# eBPF program with more generic tracing
bpf_text = """
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

struct cpu_usage_t {
    u64 cpu_time;
    u32 pid;
};

BPF_HASH(cpu_usage, u32, struct cpu_usage_t);

int trace_tick(struct pt_regs *ctx) {
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    u64 ts = bpf_ktime_get_ns();
    
    struct cpu_usage_t usage = {};
    usage.cpu_time = ts;
    usage.pid = pid;
    
    cpu_usage.update(&pid, &usage);
    return 0;
}
"""

class SystemMonitor:
    def __init__(self, export_port=8000):
        self.export_port = export_port
        
        # Prometheus metrics
        self.cpu_gauge = Gauge('system_cpu_usage', 'CPU usage percentage')
        self.memory_gauge = Gauge('system_memory_usage', 'Memory usage percentage')
        self.disk_gauge = Gauge('system_disk_usage', 'Disk usage percentage')
        
        # Initialize BPF with error handling
        try:
            self.bpf = BPF(text=bpf_text)
            
            # Try different probe points in order of preference
            probe_points = [
                "scheduler_tick",
                "pick_next_task",
                "__schedule",
                "finish_task_switch"
            ]
            
            attached = False
            for probe_point in probe_points:
                try:
                    self.bpf.attach_kprobe(event=probe_point, fn_name="trace_tick")
                    logger.info(f"Successfully attached to kernel probe: {probe_point}")
                    attached = True
                    break
                except Exception as e:
                    logger.debug(f"Failed to attach to {probe_point}: {str(e)}")
                    continue
            
            if not attached:
                raise Exception("Could not attach to any known scheduler probe points")
                
        except Exception as e:
            logger.error(f"Failed to initialize BPF: {str(e)}")
            raise

    def collect_system_metrics(self):
        while True:
            try:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                self.cpu_gauge.set(cpu_percent)
                
                # Memory usage
                memory = psutil.virtual_memory()
                self.memory_gauge.set(memory.percent)
                
                # Disk usage
                disk = psutil.disk_usage('/')
                self.disk_gauge.set(disk.percent)
                
                logger.info(f"Metrics collected - CPU: {cpu_percent}%, Memory: {memory.percent}%, Disk: {disk.percent}%")
                
                time.sleep(5)
            except Exception as e:
                logger.error(f"Error collecting metrics: {str(e)}")
                time.sleep(1)  # Avoid tight loop in case of persistent errors

    def start(self):
        # Start Prometheus HTTP server
        start_http_server(self.export_port)
        logger.info(f"Prometheus metrics server started on port {self.export_port}")
        
        # Start metrics collection in a separate thread
        metrics_thread = threading.Thread(target=self.collect_system_metrics)
        metrics_thread.daemon = True
        metrics_thread.start()

if __name__ == "__main__":
    try:
        monitor = SystemMonitor()
        monitor.start()
        
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down monitoring service")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        exit(1)
