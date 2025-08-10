# Diverse Demos

Various code examples

---

## Python API Request

```python output_only live
import requests

print("Random User Generator:\n")
response = requests.get('https://randomuser.me/api/')
data = response.json()

user = data['results'][0]
print(f"Name: {user['name']['title']} {user['name']['first']} {user['name']['last']}")
print(f"Email: {user['email']}")
print(f"Location: {user['location']['city']}, {user['location']['country']}")
```

---

## SQL Example

```sql
-- Find top customers
SELECT
    c.customer_name,
    COUNT(o.order_id) AS order_count,
    SUM(o.total) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_name
ORDER BY total_spent DESC
LIMIT 10;
```

---

## JavaScript Example

```javascript
// Simple array manipulation
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map((n) => n * 2);
console.log("Original:", numbers);
console.log("Doubled:", doubled);
```

---

## System Information

```bash
#!/bin/bash

echo "System Information:"
echo "-------------------"
echo "Hostname: $(hostname)"
echo "OS: $(uname -s)"
echo "Kernel: $(uname -r)"
echo "Uptime: $(uptime -p)"
```

---
