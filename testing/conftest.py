import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

@pytest.fixture(scope="session")
def driver():
    """Setup WebDriver - runs once before all tests"""
    
    # Chrome options
    options = Options()
    options.add_argument("--headless")  # Run without opening browser window
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1366,768")
    
    # Create driver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    # Set base path - CHANGE THIS to your actual project path
    base_path = "file:///E:/IEEE/drip/Drip/"
    
    # Store base_path for all tests
    driver.base_path = base_path
    
    yield driver
    
    # Cleanup - runs after all tests
    driver.quit()


@pytest.fixture(scope="function")
def wait_time():
    """Standard wait time for page loads"""
    return 2