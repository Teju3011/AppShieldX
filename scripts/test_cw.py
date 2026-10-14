import subprocess
import json

msg = json.dumps({"decision": "ALLOW", "riskScore": 12, "latencyMs": 4.2})

res1 = subprocess.run([
    'aws', 'logs', 'test-metric-filter',
    '--filter-pattern', '{ $.decision = "ALLOW" }',
    '--log-event-messages', msg,
    '--region', 'ap-south-1'
], capture_output=True, text=True)
print("Pattern with quotes:", res1.stdout, res1.stderr)

res2 = subprocess.run([
    'aws', 'logs', 'test-metric-filter',
    '--filter-pattern', '{ $.decision = ALLOW }',
    '--log-event-messages', msg,
    '--region', 'ap-south-1'
], capture_output=True, text=True)
print("Pattern without quotes:", res2.stdout, res2.stderr)
