import subprocess
import time

stream = f"gateway-stream-{time.strftime('%Y-%m-%d')}"
res = subprocess.run([
    'aws', 'logs', 'get-log-events',
    '--log-group-name', '/aws/appshieldx/gateway-decisions',
    '--log-stream-name', stream,
    '--limit', '4',
    '--region', 'ap-south-1'
], capture_output=True, text=True)

print("Recent Gateway Logs:")
print(res.stdout)
