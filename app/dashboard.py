from flask import Flask, render_template_string

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
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');

    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      font-family: 'DM Sans', sans-serif;
      background: #EEF4FB;
      color: #2D3748;
      padding: 40px 36px;
      min-height: 100vh;
    }

    header {
      margin-bottom: 32px;
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
    }

    .label {
      font-size: 11px;
      letter-spacing: 3px;
      color: #93AECB;
      text-transform: uppercase;
      margin-bottom: 6px;
    }

    h1 {
      font-size: 30px;
      font-weight: 700;
      color: #1A2E4A;
    }

    h1 span { color: #3B82F6; }

    .live-badge {
      display: flex;
      align-items: center;
      gap: 8px;
      background: #DBEAFE;
      border: 1px solid #BFDBFE;
      padding: 8px 16px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      color: #1D4ED8;
      letter-spacing: 1px;
    }

    .live-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #3B82F6;
      animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.3; }
    }

    /* Session Stats */
    .session-bar {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 16px;
      margin-bottom: 32px;
    }

    .stat-card {
      background: #fff;
      border: 1px solid #DBEAFE;
      border-radius: 12px;
      padding: 18px 20px;
      box-shadow: 0 1px 4px rgba(59,130,246,0.06);
    }

    .stat-label {
      font-size: 10px;
      letter-spacing: 2px;
      color: #93AECB;
      text-transform: uppercase;
      margin-bottom: 6px;
    }

    .stat-value {
      font-size: 22px;
      font-weight: 700;
      color: #1A2E4A;
    }

    .stat-value.good { color: #059669; }
    .stat-value.warn { color: #D97706; }
    .stat-value.bad { color: #DC2626; }

    /* Section Title */
    .section-title {
      font-size: 11px;
      letter-spacing: 3px;
      color: #93AECB;
      text-transform: uppercase;
      margin-bottom: 14px;
    }

    /* Device Cards */
    .devices {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-bottom: 32px;
    }

    .device-card {
      background: #fff;
      border: 1px solid #DBEAFE;
      border-radius: 12px;
      padding: 18px 24px;
      display: grid;
      grid-template-columns: 220px 1fr 1fr 1fr 1fr 120px;
      align-items: center;
      gap: 16px;
      box-shadow: 0 1px 4px rgba(59,130,246,0.05);
      transition: box-shadow 0.2s;
    }

    .device-card:hover { box-shadow: 0 4px 12px rgba(59,130,246,0.1); }
    .device-card.synced { border-left: 4px solid #10B981; }
    .device-card.degraded { border-left: 4px solid #F59E0B; }
    .device-card.offline { border-left: 4px solid #EF4444; opacity: 0.7; }

    .device-id { font-weight: 700; font-size: 15px; color: #1A2E4A; }
    .device-type { font-size: 12px; color: #93AECB; margin-top: 2px; }

    .metric-label {
      font-size: 10px;
      color: #93AECB;
      letter-spacing: 1px;
      text-transform: uppercase;
      margin-bottom: 4px;
    }

    .metric-value { font-size: 15px; color: #2D3748; font-weight: 600; }
    .metric-value.good { color: #059669; }
    .metric-value.warn { color: #D97706; }
    .metric-value.bad { color: #DC2626; }

    .status-badge {
      padding: 5px 14px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
      text-align: center;
    }

    .status-badge.synced { background: #D1FAE5; color: #065F46; }
    .status-badge.degraded { background: #FEF3C7; color: #92400E; }
    .status-badge.offline { background: #FEE2E2; color: #991B1B; }

    /* Log */
    .log-box {
      background: #fff;
      border: 1px solid #DBEAFE;
      border-radius: 12px;
      padding: 24px;
      box-shadow: 0 1px 4px rgba(59,130,246,0.05);
    }

    .log-entry {
      font-size: 13px;
      color: #64748B;
      padding: 8px 0;
      border-bottom: 1px solid #F1F5F9;
      line-height: 1.5;
      font-family: 'DM Sans', monospace;
    }

    .log-entry:last-child { border-bottom: none; }
    .log-entry .ts { color: #93AECB; margin-right: 12px; font-size: 12px; }
    .log-entry.ok .msg { color: #059669; font-weight: 500; }
    .log-entry.warn .msg { color: #D97706; font-weight: 500; }
    .log-entry.err .msg { color: #DC2626; font-weight: 500; }
  </style>
</head>
<body>

  <header>
    <div>
      <div class="label">Teleoperation Lab · Session Active</div>
      <h1>Device Validation <span>Dashboard</span></h1>
    </div>
    <div class="live-badge">
      <div class="live-dot"></div>
      LIVE
    </div>
  </header>

  <div class="session-bar">
    <div class="stat-card">
      <div class="stat-label">Session ID</div>
      <div class="stat-value" id="session-id" style="font-size:15px;">SES-20250513-001</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Devices Online</div>
      <div class="stat-value good" id="devices-online">{{ synced_count }}/{{ total_count }}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Sync Health</div>
      <div class="stat-value {% if sync_health == 'GOOD' %}good{% elif sync_health == 'DEGRADED' %}warn{% else %}bad{% endif %}" id="sync-health">{{ sync_health }}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Avg Drift</div>
      <div class="stat-value {% if avg_drift < 0.01 %}good{% elif avg_drift < 0.02 %}warn{% else %}bad{% endif %}" id="avg-drift">{{ "%.4f"|format(avg_drift) }}s</div>
    </div>
    <div class="stat-card">
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
    print("\n🚀 Dashboard running at: http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000, host="127.0.0.1")
