import subprocess
import json
import time

now = int(time.time())
start = now - 3600  # last 1 hour

res = subprocess.run([
    'aws', 'cloudwatch', 'get-metric-statistics',
    '--namespace', 'AppShieldX/Gateway',
    '--metric-name', 'AllowedTransactions',
    '--start-time', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(start)),
    '--end-time', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(now)),
    '--period', '60',
    '--statistics', 'Sum',
    '--region', 'ap-south-1'
], capture_output=True, text=True)

print("AllowedTransactions:", res.stdout)

res2 = subprocess.run([
    'aws', 'cloudwatch', 'get-metric-statistics',
    '--namespace', 'AppShieldX/Gateway',
    '--metric-name', 'BlockedThreats',
    '--start-time', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(start)),
    '--end-time', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(now)),
    '--period', '60',
    '--statistics', 'Sum',
    '--region', 'ap-south-1'
], capture_output=True, text=True)

print("BlockedThreats:", res2.stdout)
