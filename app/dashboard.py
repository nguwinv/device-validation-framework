from flask import Flask, render_template_string
import random
import time

app = Flask(__name__)

def get_devices():
    return [
        {
            "id": "VR-RIG-01",
            "type": "VR Headset",
            "status": "synced",
            "battery": 92,
            "frames_captured": 14823,
            "drift": 0.002,
            "last_sync": "0.3s ago"
        },
        {
            "id": "MC-CAM-02",
            "type": "Motion Capture Camera",
            "status": "synced",
            "battery": 78,
            "frames_captured": 14820,
            "drift": 0.004,
            "last_sync": "0.4s ago"
        },
        {
            "id": "CTRL-03",
            "type": "Teleop Controller",
            "status": "synced",
            "battery": 85,
            "frames_captured": 14823,
            "drift": 0.001,
            "last_sync": "0.2s ago"
        },
        {
            "id": "SENS-04",
            "type": "Depth Sensor",
            "status": "degraded",
            "battery": 21,
            "frames_captured": 14100,
            "drift": 0.031,
            "last_sync": "2.1s ago"
        },
        {
            "id": "CAM-05",
            "type": "RGB Camera",
            "status": "offline",
            "battery": 0,
            "frames_captured": 0,
            "drift": None,
            "last_sync": "N/A"
        },
    ]

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Tesla Device Validation Dashboard</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Courier New', monospace;
      background: #050508;
      color: #ccc;
      padding: 40px 32px;
    }
    header { margin-bottom: 36px; }
    .label {
      font-size: 10px;
      letter-spacing: 4px;
      color: #333;
      text-transform: uppercase;
      margin-bottom: 8px;
    }
    h1 { font-size: 28px; font-weight: 900; color: #fff; }
    h1 span { color: #CC0000; }

    .session-bar {
      display: flex;
      gap: 32px;
      margin-bottom: 36px;
      padding: 16px 20px;
      background: #0A0A10;
      border: 1px solid #1A1A2A;
      border-radius: 8px;
    }
    .session-bar .stat-label {
      font-size: 10px;
      color: #444;
      letter-spacing: 2px;
      text-transform: uppercase;
      margin-bottom: 4px;
    }
    .session-bar .stat-value {
      font-size: 18px;
      font-weight: 700;
      color: #fff;
    }
    .session-bar .stat-value.good { color: #00FF9C; }
    .session-bar .stat-value.warn { color: #FFD93D; }
    .session-bar .stat-value.bad { color: #FF6B6B; }

    .devices { display: flex; flex-direction: column; gap: 12px; }

    .device-card {
      padding: 18px 20px;
      background: #080810;
      border: 1px solid #1A1A2A;
      border-radius: 8px;
      display: grid;
      grid-template-columns: 200px 1fr 1fr 1fr 1fr 100px;
      align-items: center;
      gap: 16px;
    }
    .device-card.synced { border-left: 3px solid #00FF9C; }
    .device-card.degraded { border-left: 3px solid #FFD93D; }
    .device-card.offline { border-left: 3px solid #FF6B6B; opacity: 0.6; }

    .device-id { font-weight: 700; font-size: 14px; color: #fff; }
    .device-type { font-size: 11px; color: #555; margin-top: 2px; }

    .metric-label { font-size: 10px; color: #444; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 3px; }
    .metric-value { font-size: 14px; color: #bbb; font-weight: 600; }
    .metric-value.good { color: #00FF9C; }
    .metric-value.warn { color: #FFD93D; }
    .metric-value.bad { color: #FF6B6B; }

    .status-badge {
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
      text-align: center;
    }
    .status-badge.synced { background: #00FF9C22; color: #00FF9C; border: 1px solid #00FF9C44; }
    .status-badge.degraded { background: #FFD93D22; color: #FFD93D; border: 1px solid #FFD93D44; }
    .status-badge.offline { background: #FF6B6B22; color: #FF6B6B; border: 1px solid #FF6B6B44; }

    .section-title {
      font-size: 11px;
      letter-spacing: 3px;
      color: #333;
      text-transform: uppercase;
      margin-bottom: 12px;
    }

    .log-box {
      margin-top: 32px;
      padding: 20px;
      background: #080810;
      border: 1px solid #1A1A2A;
      border-radius: 8px;
    }
    .log-entry {
      font-size: 12px;
      color: #555;
      padding: 6px 0;
      border-bottom: 1px solid #0F0F18;
      line-height: 1.5;
    }
    .log-entry .ts { color: #333; margin-right: 12px; }
    .log-entry.ok .msg { color: #00FF9C; }
    .log-entry.warn .msg { color: #FFD93D; }
    .log-entry.err .msg { color: #FF6B6B; }
  </style>
</head>
<body>
  <header>
    <div class="label">Teleoperation Lab · Session Active</div>
    <h1>Device Validation <span>Dashboard</span></h1>
  </header>

  <div class="session-bar">
    <div>
      <div class="stat-label">Session ID</div>
      <div class="stat-value" id="session-id">SES-20250513-001</div>
    </div>
    <div>
      <div class="stat-label">Devices Online</div>
      <div class="stat-value good" id="devices-online">{{ synced_count }}/{{ total_count }}</div>
    </div>
    <div>
      <div class="stat-label">Sync Health</div>
      <div class="stat-value {% if sync_health == 'GOOD' %}good{% elif sync_health == 'DEGRADED' %}warn{% else %}bad{% endif %}" id="sync-health">{{ sync_health }}</div>
    </div>
    <div>
      <div class="stat-label">Avg Drift</div>
      <div class="stat-value {% if avg_drift < 0.01 %}good{% elif avg_drift < 0.02 %}warn{% else %}bad{% endif %}" id="avg-drift">{{ "%.4f"|format(avg_drift) }}s</div>
    </div>
    <div>
      <div class="stat-label">Session Status</div>
      <div class="stat-value good" id="session-status">RECORDING</div>
    </div>
  </div>

  <div class="section-title">Device Status</div>
  <div class="devices" id="device-list">
    {% for device in devices %}
    <div class="device-card {{ device.status }}" id="device-{{ device.id }}">
      <div>
        <div class="device-id">{{ device.id }}</div>
        <div class="device-type">{{ device.type }}</div>
      </div>
      <div>
        <div class="metric-label">Battery</div>
        <div class="metric-value {% if device.battery > 30 %}good{% elif device.battery > 15 %}warn{% else %}bad{% endif %}">
          {{ device.battery }}%
        </div>
      </div>
      <div>
        <div class="metric-label">Frames</div>
        <div class="metric-value">{{ "{:,}".format(device.frames_captured) }}</div>
      </div>
      <div>
        <div class="metric-label">Drift</div>
        <div class="metric-value {% if device.drift is not none %}{% if device.drift < 0.01 %}good{% elif device.drift < 0.02 %}warn{% else %}bad{% endif %}{% endif %}">
          {% if device.drift is not none %}{{ "%.3f"|format(device.drift) }}s{% else %}N/A{% endif %}
        </div>
      </div>
      <div>
        <div class="metric-label">Last Sync</div>
        <div class="metric-value">{{ device.last_sync }}</div>
      </div>
      <div>
        <span class="status-badge {{ device.status }}">{{ device.status }}</span>
      </div>
    </div>
    {% endfor %}
  </div>

  <div class="log-box">
    <div class="section-title">Session Log</div>
    <div class="log-entry ok"><span class="ts">[09:14:02]</span><span class="msg">Session SES-20250513-001 initialized. All devices polled.</span></div>
    <div class="log-entry ok"><span class="ts">[09:14:03]</span><span class="msg">VR-RIG-01 sync confirmed. Drift within threshold.</span></div>
    <div class="log-entry ok"><span class="ts">[09:14:03]</span><span class="msg">MC-CAM-02 sync confirmed. Frames aligned.</span></div>
    <div class="log-entry warn"><span class="ts">[09:14:04]</span><span class="msg">SENS-04 drift elevated: 0.031s. Flagged for review.</span></div>
    <div class="log-entry warn"><span class="ts">[09:14:04]</span><span class="msg">SENS-04 battery critical: 21%. Replace before next session.</span></div>
    <div class="log-entry err"><span class="ts">[09:14:05]</span><span class="msg">CAM-05 offline. No frames captured. Excluded from session.</span></div>
    <div class="log-entry ok"><span class="ts">[09:14:06]</span><span class="msg">Recording started. 4/5 devices active.</span></div>
  </div>
</body>
</html>
"""

@app.route("/")
def dashboard():
    devices = get_devices()
    synced = [d for d in devices if d["status"] == "synced"]
    drifts = [d["drift"] for d in devices if d["drift"] is not None]
    avg_drift = sum(drifts) / len(drifts)
    synced_count = len(synced)
    total_count = len(devices)
    sync_health = "GOOD" if synced_count >= 4 else "DEGRADED" if synced_count >= 3 else "CRITICAL"
    return render_template_string(HTML,
        devices=devices,
        synced_count=synced_count,
        total_count=total_count,
        sync_health=sync_health,
        avg_drift=avg_drift
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="127.0.0.1")
