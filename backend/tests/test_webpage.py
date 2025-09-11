import os
import time
import httpx


def _get_env(name: str, default: str) -> str:
    value = os.getenv(name)
    return value if value else default


def test_click_displays_test_ping_to_the_right(page):
    """
    E2E: Verify that clicking the button shows the backend TEST_PING value
    to the right of the button on the page.

    Requirements:
    - pytest-playwright must be installed; run with `pytest -q` and the plugin will
      provide the `page` fixture.
    - The frontend and backend services must be running and reachable.

    Environment variables (optional):
    - FRONTEND_URL (default: http://localhost:5173)
    - BACKEND_URL  (default: http://localhost:8000)
    """

    frontend_url = _get_env("FRONTEND_URL", "http://localhost:5173")
    backend_url = _get_env("BACKEND_URL", "http://localhost:8000")

    # Fetch the expected TEST_PING value from the backend itself so the test
    # does not need to import application code or hardcode the value.
    resp = httpx.get(f"{backend_url}/ping", timeout=10.0)
    resp.raise_for_status()
    expected_message = resp.json()["message"]

    # Navigate to the frontend
    page.goto(frontend_url, wait_until="domcontentloaded")

    # Locate the button and capture its position
    button = page.get_by_role("button", name="Click me")
    button.wait_for(state="visible")
    button_box = button.bounding_box()
    assert button_box is not None, "Failed to read button bounding box"

    # Click the button to trigger the fetch and render of the message
    button.click()

    # Wait for the message text to appear
    message_locator = page.get_by_text(expected_message, exact=True)
    message_locator.wait_for(state="visible", timeout=5000)

    # Validate the message content
    assert message_locator.inner_text() == expected_message

    # Validate the message is rendered to the right of the button
    msg_box = message_locator.bounding_box()
    assert msg_box is not None, "Failed to read message bounding box"

    # Strictly to the right in the x-axis
    assert msg_box["x"] > button_box["x"], (
        f"Message should be to the right of the button (msg.x={msg_box['x']}, "
        f"btn.x={button_box['x']})"
    )

    # And not above the button (a loose vertical alignment check)
    assert msg_box["y"] <= button_box["y"] + button_box["height"], (
        f"Message appears below the button (msg.y={msg_box['y']}, "
        f"btn.y+height={button_box['y'] + button_box['height']})"
    )


