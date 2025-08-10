# System Dashboard

Real-time system monitoring

remember to install psutil

# pip install psutil

---

## Current Status

```python output_only live
import psutil
import time

def format_bar(percent):
    filled = '▮' * int(percent/5)
    empty = '▯' * (20 - len(filled))
    return f"[{filled}{empty}]"

print(f"{'Metric':<20} | {'Value':<15} | Usage")
print("-" * 50)

try:
    # CPU
    cpu = psutil.cpu_percent()
    print(f"{'CPU Usage':<20} | {f'{cpu}%':<15} | {format_bar(cpu)}")

    # Memory
    mem = psutil.virtual_memory()
    print(f"{'Memory Usage':<20} | {f'{mem.percent}%':<15} | {format_bar(mem.percent)}")

    # Disk
    disk = psutil.disk_usage('/')
    print(f"{'Disk Usage':<20} | {f'{disk.percent}%':<15} | {format_bar(disk.percent)}")

    # Network
    net = psutil.net_io_counters()
    print(f"\nNetwork Stats:")
    print(f"  Sent: {net.bytes_sent/1024/1024:.2f} MB")
    print(f"  Recv: {net.bytes_recv/1024/1024:.2f} MB")
    print(f"\nUpdated: {time.strftime('%H:%M:%S')}")

except Exception as e:
    print(f"\nError: {str(e)}")
    print("Please ensure psutil is installed: pip install psutil")
```

---

# Live System Monitoring

Press 'r' to refresh
