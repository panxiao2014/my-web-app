import pytest
from playwright.sync_api import Page, expect
import subprocess
import time
import os
import sys
import signal

# Backend and Frontend process handles
backend_process = None
frontend_process = None


def _popen_kwargs(cwd: str):
    """
    Return platform-safe Popen kwargs for process group/session handling
    """
    kwargs = {"cwd": cwd}

    if sys.platform == "win32":
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
        kwargs["shell"] = False
    else:
        # Linux / macOS
        kwargs["start_new_session"] = True

    return kwargs


def _terminate_process(proc: subprocess.Popen):
    """
    Gracefully terminate a subprocess cross-platform
    """
    if proc is None:
        return

    try:
        if sys.platform == "win32":
            proc.send_signal(signal.CTRL_BREAK_EVENT)
        else:
            os.killpg(proc.pid, signal.SIGTERM)
    except Exception:
        proc.terminate()

    proc.wait(timeout=10)


@pytest.fixture(scope="session", autouse=True)
def start_servers():
    """
    Start backend and frontend servers before running tests
    """
    global backend_process, frontend_process

    base_dir = os.path.dirname(__file__)

    # -------- Start backend --------
    backend_process = subprocess.Popen(
        ["uvicorn", "main:app", "--port", "8000"],
        **_popen_kwargs(cwd=base_dir),
    )

    # -------- Start frontend --------
    frontend_dir = os.path.join(base_dir, "..", "frontend")

    frontend_cmd = ["npm", "run", "dev"]
    if sys.platform == "win32":
        # npm.cmd is needed on Windows
        frontend_cmd = ["npm.cmd", "run", "dev"]

    frontend_process = subprocess.Popen(
        frontend_cmd,
        cwd=frontend_dir,
        start_new_session=(sys.platform != "win32"),
        shell=(sys.platform == "win32"),
    )

    # Wait for servers to start
    time.sleep(5)

    yield

    # -------- Cleanup --------
    _terminate_process(frontend_process)
    _terminate_process(backend_process)


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
