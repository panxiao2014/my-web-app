import pytest
from playwright.sync_api import Page, expect

@pytest.mark.zhongkao
class TestZhongkao:
    """
    Test cases for Zhongkao
    """
    
    def test_name_validation_with_leading_space(self, page: Page):
        """
        Test that inputting a name with leading space shows warning
        and disables the Next button
        """
        # Navigate to the application
        page.goto("http://localhost:5173")
        
        # Click on Zhongkao navigation button
        page.click("text=中考")
        
        # Wait for Zhongkao to load
        expect(page.locator("h1")).to_have_text("User Registration")
        
        # Verify we're on page 1
        expect(page.locator(".zhongkao-page-indicator")).to_contain_text("Page 1 of 2")
        
        # Verify Next button is initially disabled (no input yet)
        next_button = page.locator("button:has-text('Next')")
        expect(next_button).to_be_disabled()
        
        # Input a name with leading space
        name_input = page.locator(".zhongkao-input-field")
        name_input.fill(" John")
        
        # Verify error message appears
        error_message = page.locator(".zhongkao-error-message")
        expect(error_message).to_be_visible()
        expect(error_message).to_have_text("Name should not begin with empty spaces")
        
        # Verify Next button is still disabled
        expect(next_button).to_be_disabled()
        
    def test_name_validation_with_valid_input(self, page: Page):
        """
        Test that inputting a valid name enables the Next button
        """
        # Navigate to the application
        page.goto("http://localhost:5173")
        
        # Click on Zhongkao navigation button
        page.click("text=中考")
        
        # Wait for Zhongkao to load
        expect(page.locator("h1")).to_have_text("User Registration")
        
        # Input a valid name
        name_input = page.locator(".zhongkao-input-field")
        name_input.fill("John")
        
        # Verify no error message appears
        error_message = page.locator(".zhongkao-error-message")
        expect(error_message).not_to_be_visible()
        
        # Verify Next button is enabled
        next_button = page.locator("button:has-text('Next')")
        expect(next_button).to_be_enabled()
        
    def test_navigation_between_pages(self, page: Page):
        """
        Test navigation between pages preserves user input
        """
        # Navigate to the application
        page.goto("http://localhost:5173")
        
        # Click on Zhongkao navigation button
        page.click("text=中考")
        
        # Wait for Zhongkao to load
        expect(page.locator("h1")).to_have_text("User Registration")
        
        # Input a valid name on page 1
        name_input = page.locator(".zhongkao-input-field")
        name_input.fill("John")
        
        # Click Next to go to page 2
        next_button = page.locator("button:has-text('Next')")
        next_button.click()
        
        # Verify we're on page 2
        expect(page.locator(".zhongkao-page-indicator")).to_contain_text("Page 2 of 2")
        
        # Verify Previous button is enabled
        previous_button = page.locator("button:has-text('Previous')")
        expect(previous_button).to_be_enabled()
        
        # Select gender
        gender_select = page.locator(".zhongkao-select-field")
        gender_select.select_option("Female")
        
        # Go back to page 1
        previous_button.click()
        
        # Verify we're back on page 1
        expect(page.locator(".zhongkao-page-indicator")).to_contain_text("Page 1 of 2")
        
        # Verify name is still there
        name_input = page.locator(".zhongkao-input-field")
        expect(name_input).to_have_value("John")