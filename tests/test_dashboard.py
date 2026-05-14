import pytest
from selenium.webdriver.common.by import By
from utils.config import BASE_URL, EXPECTED_DEVICES

def test_dashboard_loads(driver):
    driver.get(BASE_URL)
    assert "Device Validation Dashboard" in driver.title or "Device Validation" in driver.page_source

def test_all_devices_present(driver):
    driver.get(BASE_URL)
    page = driver.page_source
    for device_id in EXPECTED_DEVICES:
        assert device_id in page, f"Device {device_id} not found on dashboard"

def test_session_id_displayed(driver):
    driver.get(BASE_URL)
    session = driver.find_element(By.ID, "session-id")
    assert session.text.startswith("SES-"), f"Unexpected session ID: {session.text}"

def test_sync_health_displayed(driver):
    driver.get(BASE_URL)
    health = driver.find_element(By.ID, "sync-health")
    assert health.text in ["GOOD", "DEGRADED", "CRITICAL"], f"Invalid sync health: {health.text}"

def test_session_status_is_recording(driver):
    driver.get(BASE_URL)
    status = driver.find_element(By.ID, "session-status")
    assert status.text == "RECORDING"

def test_devices_online_count_displayed(driver):
    driver.get(BASE_URL)
    count = driver.find_element(By.ID, "devices-online")
    assert "/" in count.text, f"Expected format X/Y, got: {count.text}"

def test_offline_device_flagged(driver):
    driver.get(BASE_URL)
    page = driver.page_source
    assert "offline" in page.lower(), "No offline device detected on dashboard"

def test_degraded_device_flagged(driver):
    driver.get(BASE_URL)
    page = driver.page_source
    assert "degraded" in page.lower(), "No degraded device detected on dashboard"
