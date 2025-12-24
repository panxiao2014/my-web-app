import pytest
from playwright.sync_api import Page, expect

@pytest.mark.app1
class TestApp1:
    """
    Test cases for App1
    """
    
    def test_button_click_returns_pong(self, page: Page):
        """
        Test that clicking the button in App1 returns 'pong!' response
        """
        # Navigate to the application
        page.goto("http://localhost:5173")
        
        # Click on App1 navigation button
        page.click("[data-testid='nav-app1']")
        
        # Wait for App1 to load
        expect(page.locator("h1")).to_have_text("App1")
        
        # Click the "Click Me" button
        page.click("button:has-text('Click Me')")
        
        # Wait for response to appear
        response_element = page.locator(".app1-response")
        expect(response_element).to_be_visible()
        
        # Verify the response text is "pong!"
        expect(response_element).to_have_text("pong!")