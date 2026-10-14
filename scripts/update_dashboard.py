import subprocess
import json

dashboard_body = {
    "widgets": [
        {
            "type": "text",
            "x": 0,
            "y": 0,
            "width": 24,
            "height": 2,
            "properties": {
                "markdown": "# AppShieldX: Cloud-Native Zero-Trust Mobile Security Framework\n**Region:** Asia Pacific (Mumbai) ap-south-1 | **EC2 Instance:** i-009b430e483e519a4 (65.1.181.179) | **Account:** 989585887382 | **Mode:** Live Evaluation Stream"
            }
        },
        {
            "type": "metric",
            "x": 0,
            "y": 2,
            "width": 12,
            "height": 6,
            "properties": {
                "metrics": [
                    ["AppShieldX/Gateway", "AllowedTransactions", {"stat": "Sum", "color": "#2ca02c", "label": "ALLOW (HTTP 200)"}],
                    ["AppShieldX/Gateway", "BlockedThreats", {"stat": "Sum", "color": "#d62728", "label": "BLOCKED / QUARANTINED (HTTP 403)"}]
                ],
                "view": "timeSeries",
                "stacked": False,
                "region": "ap-south-1",
                "title": "Zero-Trust Policy Enforcement Point (PEP) Decisions",
                "period": 60
            }
        },
        {
            "type": "metric",
            "x": 12,
            "y": 2,
            "width": 6,
            "height": 6,
            "properties": {
                "metrics": [
                    ["AppShieldX/Gateway", "GatewayLatencyMs", {"stat": "Average", "color": "#ff7f0e", "label": "Inspection Overhead (ms)"}]
                ],
                "view": "singleValue",
                "region": "ap-south-1",
                "title": "Gateway Mean Inspection Latency",
                "period": 60
            }
        },
        {
            "type": "metric",
            "x": 18,
            "y": 2,
            "width": 6,
            "height": 6,
            "properties": {
                "metrics": [
                    ["AppShieldX/Gateway", "DeviceRiskScore", {"stat": "Maximum", "color": "#9467bd", "label": "Peak Risk Score"}]
                ],
                "view": "singleValue",
                "region": "ap-south-1",
                "title": "Peak Device Risk Score (R ∈ [0, 100])",
                "period": 60
            }
        },
        {
            "type": "log",
            "x": 0,
            "y": 8,
            "width": 12,
            "height": 10,
            "properties": {
                "query": "SOURCE '/aws/appshieldx/gateway-decisions' | fields @timestamp, @message | sort @timestamp desc | limit 25",
                "region": "ap-south-1",
                "title": "Live Gateway Audit Log (Zero-Trust Interceptions)",
                "view": "table"
            }
        },
        {
            "type": "log",
            "x": 12,
            "y": 8,
            "width": 12,
            "height": 10,
            "properties": {
                "query": "SOURCE '/aws/appshieldx/threat-events' | fields @timestamp, @message | sort @timestamp desc | limit 25",
                "region": "ap-south-1",
                "title": "Mobile Threat Telemetry Stream (RASP Ingest)",
                "view": "table"
            }
        },
        {
            "type": "metric",
            "x": 0,
            "y": 18,
            "width": 24,
            "height": 5,
            "properties": {
                "metrics": [
                    ["AWS/EC2", "CPUUtilization", "InstanceId", "i-009b430e483e519a4", {"stat": "Average", "label": "EC2 CPU (%)"}],
                    ["AWS/EC2", "NetworkIn", "InstanceId", "i-009b430e483e519a4", {"stat": "Sum", "yAxis": "right", "label": "Network In (Bytes)"}],
                    ["AWS/EC2", "NetworkOut", "InstanceId", "i-009b430e483e519a4", {"stat": "Sum", "yAxis": "right", "label": "Network Out (Bytes)"}]
                ],
                "view": "timeSeries",
                "region": "ap-south-1",
                "title": "EC2 Host Compute Health & Gateway Throughput",
                "period": 60
            }
        }
    ]
}

res = subprocess.run([
    'aws', 'cloudwatch', 'put-dashboard',
    '--dashboard-name', 'AppShieldX-Executive-SOC',
    '--dashboard-body', json.dumps(dashboard_body),
    '--region', 'ap-south-1'
], capture_output=True, text=True)

print("Put Dashboard result:", res.stdout, res.stderr)
