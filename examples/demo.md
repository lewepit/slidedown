# Welcome to Slidedown!

Terminal-based Markdown Presentations

---

## Core Features

- **Live Code Execution**: Run Python directly in slides
- **Theming Support**: Multiple color schemes
- **Keyboard Navigation**: Simple controls
- **Responsive Layout**: Adapts to terminal size
- **Markdown Formatting**: Headers, lists, code blocks

Try pressing `t` to change themes during the presentation!

---

## Live Data Visualization

```python live
import time
import random

print("Real-time Sensor Data\n")
print(" Time  | Value | Graph")
print("----------------------")

for i in range(1, 11):
    value = random.randint(20, 80)
    time_str = f"{i}s"
    bar = '▉' * int(value/10) + '-' * (8 - int(value/10))
    print(f" {time_str:4} | {value:5} | {bar}")
    time.sleep(0.5)
```

---

## System Information

```python live
import platform
import datetime

print("System Report:")
print(f"OS: {platform.system()} {platform.release()}")
print(f"Python: {platform.python_version()}")
print(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}")
print("\nCPU Cores: ", end='')
try:
    import os
    print(os.cpu_count())
except:
    print("N/A")

print("\nDisk Usage:")
try:
    import shutil
    usage = shutil.disk_usage('/')
    print(f"Total: {usage.total // (1024**3)} GB")
    print(f"Used: {usage.used // (1024**3)} GB")
    print(f"Free: {usage.free // (1024**3)} GB")
except:
    print("Unavailable")
```

---

## ASCII Art Generator

```python live
import random

print("Random ASCII Art:\n")

arts = [
    r"""
      .--.
     |o_o |
     |:_/ |
    //   \ \
   (|     | )
  /'\_   _/`\
  \___)=(___/
    """,
    r"""
      /\_/\
     ( o.o )
      > ^ <
    """,
    r"""
       __
      UooU\.'@@@@@@`.
      \__/(@@@@@@@@@@)
        (@@@@@@@@)
        `YY~~~~YY'
         ||    ||
    """
]

print(random.choice(arts))
```

---

## Network Check

```python live
import socket
import time

services = [
    ("Google", "8.8.8.8", 53),
    ("Cloudflare", "1.1.1.1", 53),
    ("GitHub SSH", "github.com", 22),
    ("Localhost", "127.0.0.1", 80)
]

print("Network Connectivity Test:\n")
for name, host, port in services:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try:
        s.connect((host, port))
        status = "✓ ONLINE"
    except:
        status = "✗ OFFLINE"

    print(f"{name:12} {host:15}:{port:<5} {status}")
    time.sleep(0.7)

print("\nTest complete!")
```

---

## Math Visualization

```python live
import math

print("Trigonometry Visualization\n")
print(" Angle | Sin     | Cos     | Graph")
print("----------------------------------")

for angle in range(0, 360, 30):
    rad = math.radians(angle)
    sin_val = math.sin(rad)
    cos_val = math.cos(rad)

    # Create visualization
    sin_graph = '■' * int((sin_val ) * 15)
    cos_graph = '□' * int((cos_val ) * 15)

    print(f" {angle:4}° | {sin_val:7.3f} | {cos_val:7.3f} | {sin_graph}")
    print(f"       |         |         | {cos_graph}")
```

---

# Thank You!

Try creating your own presentations!
