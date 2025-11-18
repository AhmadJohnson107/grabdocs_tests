import os
import time
from pathlib import Path
import shutil

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ========== CONFIG ==========
CONFIG = {
    "base_url": "https://app.grabdocs.com",
    # You need test credentials — these are placeholders
    "username": os.getenv("GRABDOCS_USER", "your_email@example.com"),
    "password": os.getenv("GRABDOCS_PASS", "YourPassword"),
    "headless": False,
    "timeout": 20,

