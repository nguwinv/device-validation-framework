# Device Validation Dashboard & Test Framework

[![Device Validation UI Tests](https://github.com/nguwinv/device-validation-framework/actions/workflows/ui-tests.yml/ui-tests.yml)](https://github.com/nguwinv/device-validation-framework/actions/workflows/ui-tests.yml)

A Selenium-based UI test framework built around a mock teleoperation device monitoring dashboard — modeled after multi-device VR and motion-capture validation work at Tesla.

## Tech Stack
- Python, Flask, Selenium, pytest, pytest-html, GitHub Actions

## Test Coverage
| Suite | What it tests |
|---|---|
| test_dashboard.py | Dashboard loads, all devices present, session ID, sync health, recording status, online count, offline/degraded detection |

## Bugs This Would Catch
- Device sync status not updating correctly
- Offline or degraded devices not being flagged on the dashboard
- Session ID missing or malformed
- Recording status stuck or incorrect
- Drift thresholds not reflected in the UI

## How to Run

**Terminal 1 — start the dashboard:**

