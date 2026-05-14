import pytest
import os
from utils.driver import get_driver

@pytest.fixture
def driver():
    driver = get_driver(headless=False)
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            os.makedirs("reports/screenshots", exist_ok=True)
            path = f"reports/screenshots/{item.name}.png"
            driver.save_screenshot(path)
            print(f"\nScreenshot saved: {path}")
