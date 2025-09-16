import pytest
from playwright.sync_api import Page, expect

from app.config.config import TEST_PING


@pytest.mark.e2e
def test_click_button_displays_test_ping(page: Page):
    # Open the frontend app
    page.goto("http://localhost:5173/")

    # Click the button labeled "Click me"
    page.get_by_role("button", name="Click me").click()

    # Expect the TEST_PING text to become visible
    expect(page.get_by_text(TEST_PING)).to_be_visible()

    # Additionally, verify that the TEST_PING text is displayed to the right of the button
    button = page.get_by_role("button", name="Click me")
    resp_text = page.get_by_text(TEST_PING)

    # Get bounding boxes for both elements
    button_box = button.bounding_box()
    resp_box = resp_text.bounding_box()

    # Assert that the TEST_PING text is to the right of the button
    assert button_box is not None and resp_box is not None, "Could not get bounding boxes"
    assert resp_box["x"] > button_box["x"] + button_box["width"], "TEST_PING text is not to the right of the button"
    
    # Also verify they are on the same vertical position
    button_center_y = button_box["y"] + button_box["height"] / 2
    resp_center_y = resp_box["y"] + resp_box["height"] / 2
    assert abs(button_center_y - resp_center_y) < 5, "TEST_PING text is not aligned vertically with the button"


@pytest.mark.e2e
def test_click_show_me_a_user_button_displays_user_info(page: Page):
    # Open the frontend app
    page.goto("http://localhost:5173/")

    # Click the button labeled "Show me a user"
    page.get_by_role("button", name="Show me a user").click()

    # Wait for the user information to be displayed in the specific user display area
    # Use the new data-testid for more reliable targeting
    user_display_area = page.get_by_test_id("user-display-content")
    expect(user_display_area).to_be_visible()
    
    # Verify that the user information is displayed in the correct container
    # Check for the specific user data labels within the user display area
    expect(user_display_area.get_by_text("Name:")).to_be_visible()
    expect(user_display_area.get_by_text("Gender:")).to_be_visible()
    expect(user_display_area.get_by_text("Age:")).to_be_visible()

    # Verify that the user information is displayed in the correct format
    # The text should be in the format: "Name: [name]", "Gender: [gender]", "Age: [age]"
    user_info_container = user_display_area.locator("div:has-text('Name:')").first
    expect(user_info_container).to_be_visible()
    
    # Verify that the "No user selected yet." text is no longer visible
    expect(page.get_by_text("No user selected yet.")).not_to_be_visible()



