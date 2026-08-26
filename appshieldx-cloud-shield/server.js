const http = require('http');
const crypto = require('crypto');
const JWT_SECRET = 'appshieldx_super_secure_secret_key_2026';

const logsStore = [];

const server = http.createServer((req, res) => {
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // 1. Health Endpoint
  if (req.url === '/v1/status' && req.method === 'GET') {
    res.writeHead(200);
    res.end(JSON.stringify({ gateway: 'ONLINE', serviceMesh: 'ACTIVE' }));
  }

  // 2. Authentication Route
  else if (req.url === '/v1/auth/login' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const parsed = JSON.parse(body || '{}');
        const deviceId = parsed.deviceId || 'UNKNOWN_DEVICE';

        const b64 = (obj) => Buffer.from(JSON.stringify(obj)).toString('base64url');
        const header = b64({ alg: 'HS256', typ: 'JWT' });
        const payload = b64({ deviceId: deviceId, exp: Math.floor(Date.now() / 1000) + 3600 });

        const signature = crypto.createHmac('sha256', JWT_SECRET).update(header + '.' + payload).digest('base64url');
        const token = header + '.' + payload + '.' + signature;

        console.log('[Auth] Issued JWT for Device:', deviceId);
        res.writeHead(200);
        res.end(JSON.stringify({ accessToken: token }));
      } catch (e) {
        res.writeHead(400);
        res.end(JSON.stringify({ error: 'Malformed payload' }));
      }
    });
  }

  // 3. Protected Telemetry Route
  else if (req.url === '/v1/telemetry' && req.method === 'POST') {
    const auth = req.headers['authorization'];
    if (!auth || !auth.startsWith('Bearer ')) {
      res.writeHead(401);
      res.end(JSON.stringify({ error: 'Unauthorized' }));
      return;
    }

    const token = auth.split(' ')[1];
    const parts = token.split('.');
    if (parts.length !== 3) {
      res.writeHead(403);
      res.end(JSON.stringify({ error: 'Forbidden' }));
      return;
    }

    const [header, payload, signature] = parts;
    const expectedSig = crypto.createHmac('sha256', JWT_SECRET).update(header + '.' + payload).digest('base64url');

    if (signature !== expectedSig) {
      res.writeHead(403);
      res.end(JSON.stringify({ error: 'Forbidden: Signature mismatch' }));
      return;
    }

    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const telemetry = JSON.parse(body || '{}');
        const entry = {
          id: logsStore.length + 1,
          timestamp: new Date().toISOString(),
          deviceId: telemetry.deviceId || 'UNKNOWN',
          fridaDetected: telemetry.fridaHookDetected || false,
          integrityVerified: telemetry.integrityVerified || false,
          threatMitigated: telemetry.threatMitigated || false,
          ip: req.socket.remoteAddress
        };

        logsStore.unshift(entry);
        if (logsStore.length > 50) logsStore.pop();

        console.log('[Telemetry Recorded]', entry);
        res.writeHead(200);
        res.end(JSON.stringify({ status: 'SUCCESS', message: 'Telemetry received' }));
      } catch (e) {
        res.writeHead(400);
        res.end(JSON.stringify({ error: 'Bad Payload' }));
      }
    });
  }

  // 4. Admin Dashboard API
  else if (req.url === '/v1/admin/logs' && req.method === 'GET') {
    res.writeHead(200);
    res.end(JSON.stringify(logsStore));
  }

  // 5. Admin Web Dashboard Page
  else if (req.url === '/dashboard' && req.method === 'GET') {
    res.setHeader('Content-Type', 'text/html');
    res.writeHead(200);
    res.end(`
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>AppShieldX Security Control Panel</title>
        <style>
          body { background: #0f0f12; color: #c0caf5; font-family: monospace; padding: 24px; }
          h1 { color: #7aa2f7; margin-bottom: 4px; }
          .subtitle { color: #565f89; margin-bottom: 24px; }
          table { width: 100%; border-collapse: collapse; background: #16161e; border-radius: 8px; overflow: hidden; }
          th, td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #222230; }
          th { background: #1a1b26; color: #7aa2f7; }
          .badge-danger { color: #f7768e; font-weight: bold; }
          .badge-success { color: #9ece6a; font-weight: bold; }
        </style>
      </head>
      <body>
        <h1>🛡️ AppShieldX Core — Web Admin Dashboard</h1>
        <div class="subtitle">Live Threat Telemetry Ingestion Monitoring Console</div>
        <table>
          <thead>
            <tr>
              <th>Time</th>
              <th>Device ID</th>
              <th>Frida Hook</th>
              <th>Integrity</th>
              <th>Mitigated</th>
            </tr>
          </thead>
          <tbody id="logs"></tbody>
        </table>
        <script>
          async function fetchLogs() {
            const res = await fetch('/v1/admin/logs');
            const logs = await res.json();
            const tbody = document.getElementById('logs');
            tbody.innerHTML = logs.map(l => \`
              <tr>
                <td>\${l.timestamp.split('T')[1].split('.')[0]}</td>
                <td>\${l.deviceId}</td>
                <td class="\${l.fridaDetected ? 'badge-danger' : 'badge-success'}">\${l.fridaDetected ? 'DETECTED' : 'CLEAR'}</td>
                <td class="\${l.integrityVerified ? 'badge-success' : 'badge-danger'}">\${l.integrityVerified ? 'VERIFIED' : 'FAILED'}</td>
                <td class="\${l.threatMitigated ? 'badge-danger' : 'badge-success'}">\${l.threatMitigated ? 'YES' : 'NO'}</td>
              </tr>
            \`).join('');
          }
          setInterval(fetchLogs, 2000);
          fetchLogs();
        </script>
      </body>
      </html>
    `);
  } else {
    res.writeHead(404);
    res.end(JSON.stringify({ error: 'Route not found' }));
  }
});

server.listen(8080, '0.0.0.0', () => console.log('AppShieldX Gateway & Web Dashboard live on http://localhost:8080/dashboard'));