import pytest
from playwright.sync_api import Page, expect
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from config.app_config import ZHONGKAO_CONFIG, COMMON_CONFIG, format_page_indicator

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
        page.click("[data-testid='nav-zhongkao']")
        
        # Wait for Zhongkao to load
        expect(page.locator("h1")).to_have_text(ZHONGKAO_CONFIG['title'])
        
        # Verify we're on page 1
        page_indicator_text = format_page_indicator(1, 2)
        expect(page.locator(".zhongkao-page-indicator")).to_contain_text(page_indicator_text)
        
        # Verify Next button is initially disabled (no input yet)
        next_button_text = COMMON_CONFIG['navigation']['nextButton']
        next_button = page.locator(f"button:has-text('{next_button_text}')")
        expect(next_button).to_be_disabled()
        
        # Input a name with leading space
        name_input = page.locator(".zhongkao-input-field")
        name_input.fill(" John")
        
        # Verify error message appears
        error_message = page.locator(".zhongkao-error-message")
        expect(error_message).to_be_visible()
        expected_error = COMMON_CONFIG['validation']['name']['leadingSpace']
        expect(error_message).to_have_text(expected_error)
        
        # Verify Next button is still disabled
        expect(next_button).to_be_disabled()
        
    def test_name_validation_with_valid_input(self, page: Page):
        """
        Test that inputting a valid name enables the Next button
        """
        # Navigate to the application
        page.goto("http://localhost:5173")
        
        # Click on Zhongkao navigation button
        page.click("[data-testid='nav-zhongkao']")
        
        # Wait for Zhongkao to load
        expect(page.locator("h1")).to_have_text(ZHONGKAO_CONFIG['title'])
        
        # Input a valid name
        name_input = page.locator(".zhongkao-input-field")
        name_input.fill("John")
        
        # Verify no error message appears
        error_message = page.locator(".zhongkao-error-message")
        expect(error_message).not_to_be_visible()
        
        # Verify Next button is enabled
        next_button_text = COMMON_CONFIG['navigation']['nextButton']
        next_button = page.locator(f"button:has-text('{next_button_text}')")
        expect(next_button).to_be_enabled()
        
    def test_navigation_between_pages(self, page: Page):
        """
        Test navigation between pages preserves user input
        """
        # Navigate to the application
        page.goto("http://localhost:5173")
        
        # Click on Zhongkao navigation button
        page.click("[data-testid='nav-zhongkao']")
        
        # Wait for Zhongkao to load
        expect(page.locator("h1")).to_have_text(ZHONGKAO_CONFIG['title'])
        
        # Input a valid name on page 1
        name_input = page.locator(".zhongkao-input-field")
        name_input.fill("John")
        
        # Click Next to go to page 2
        next_button_text = COMMON_CONFIG['navigation']['nextButton']
        next_button = page.locator(f"button:has-text('{next_button_text}')")
        next_button.click()
        
        # Verify we're on page 2
        page_indicator_text = format_page_indicator(2, 2)
        expect(page.locator(".zhongkao-page-indicator")).to_contain_text(page_indicator_text)
        
        # Verify Previous button is enabled
        previous_button_text = COMMON_CONFIG['navigation']['previousButton']
        previous_button = page.locator(f"button:has-text('{previous_button_text}')")
        expect(previous_button).to_be_enabled()
        
        # Select gender
        gender_select = page.locator(".zhongkao-select-field")
        gender_select.select_option(ZHONGKAO_CONFIG['pages']['page2']['options'][0])
        
        # Go back to page 1
        previous_button.click()
        
        # Verify we're back on page 1
        page_indicator_text = format_page_indicator(1, 2)
        expect(page.locator(".zhongkao-page-indicator")).to_contain_text(page_indicator_text)
        
        # Verify name is still there
        name_input = page.locator(".zhongkao-input-field")
        expect(name_input).to_have_value("John")