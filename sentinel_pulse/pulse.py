import time
import psutil

class PulseMonitor:
    """Sentinel-Pulse (handled by Feb). Monitoring health and resource usage."""

    def __init__(self):
        self.start_time = time.time()

    def get_resource_usage(self):
        """Returns CPU and Memory usage for the agent process."""
        try:
            process = psutil.Process()
            cpu_percent = process.cpu_percent(interval=1.0)
            memory_info = process.memory_info()
            return {
                "cpu_percent": cpu_percent,
                "memory_mb": memory_info.rss / (1024 * 1024),
                "uptime_seconds": time.time() - self.start_time
            }
        except Exception as e:
            return {"error": str(e)}

    def heartbeat(self):
        """A simple heartbeat to confirm the monitor is alive."""
        print(f"[Pulse] Heartbeat at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        return True

if __name__ == "__main__":
    pulse = PulseMonitor()
    while True:
        pulse.heartbeat()
        print(f"Usage: {pulse.get_resource_usage()}")
        time.sleep(60) # Log every minute
