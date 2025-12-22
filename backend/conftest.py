import pytest
from playwright.sync_api import Page, expect
import subprocess
import time
import signal
import os

# Backend and Frontend process handles
backend_process = None
frontend_process = None

@pytest.fixture(scope="session", autouse=True)
def start_servers():
    """
    Start backend and frontend servers before running tests
    """
    global backend_process, frontend_process
    
    # Start backend server
    backend_process = subprocess.Popen(
        ["uvicorn", "main:app", "--port", "8000"],
        cwd=os.path.join(os.path.dirname(__file__)),
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )
    
    # Start frontend server
    frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=frontend_dir,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        shell=True
    )
    
    # Wait for servers to start
    time.sleep(5)
    
    yield
    
    # Cleanup: Stop servers after all tests
    if backend_process:
        os.kill(backend_process.pid, signal.CTRL_BREAK_EVENT)
        backend_process.wait()
    
    if frontend_process:
        os.kill(frontend_process.pid, signal.CTRL_BREAK_EVENT)
        frontend_process.wait()


@pytest.fixture(scope="function")
def page(playwright):
    """
    Create a new browser page for each test
    """
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    yield page
    
    context.close()
    browser.close()