import subprocess
import json
import time

now = int(time.time())
start = now - 3600

res1 = subprocess.run([
    'aws', 'cloudwatch', 'get-metric-statistics',
    '--namespace', 'AppShieldX/Gateway',
    '--metric-name', 'GatewayLatencyMs',
    '--start-time', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(start)),
    '--end-time', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(now)),
    '--period', '300',
    '--statistics', 'Average',
    '--region', 'ap-south-1'
], capture_output=True, text=True)
print("GatewayLatencyMs:", res1.stdout)

res2 = subprocess.run([
    'aws', 'cloudwatch', 'get-metric-statistics',
    '--namespace', 'AppShieldX/Gateway',
    '--metric-name', 'DeviceRiskScore',
    '--start-time', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(start)),
    '--end-time', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(now)),
    '--period', '300',
    '--statistics', 'Maximum',
    '--region', 'ap-south-1'
], capture_output=True, text=True)
print("DeviceRiskScore:", res2.stdout)
