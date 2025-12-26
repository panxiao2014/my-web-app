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
    
    @pytest.mark.parametrize("input_value,should_be_valid,error_key", [
        # Invalid cases
        (" John", False, "leadingSpace"),
        ("John ", False, "trailingSpace"),
        ("J", False, "tooShort"),
        ("a" * 51, False, "tooLong"),
        ("John123", False, "containsNumbers"),
        ("John@Doe", False, "invalidCharacters"),
        ("John  Doe", False, "multipleSpaces"),
        ("-John", False, "startsWithSpecial"),
        ("John'", False, "endsWithSpecial"),
        
        # Valid cases
        ("John", True, None),
        ("Mary Jane", True, None),
        ("O'Brien", True, None),
        ("Jean-Luc", True, None),
        ("李明", True, None),
        ("José García", True, None),
    ])
    def test_name_validation_with_various_inputs(self, page: Page, input_value: str, should_be_valid: bool, error_key: str):
        """
        Test that various valid and invalid name inputs show correct validation behavior
        """
        # Navigate to the application
        page.goto("http://localhost:5173")
        
        # Click on Zhongkao navigation button
        page.click("[data-testid='nav-zhongkao']")
        
        # Wait for Zhongkao to load
        title = page.locator("[data-testid='zhongkao-title']")
        expect(title).to_have_text(ZHONGKAO_CONFIG['title'])
        
        name_input = page.locator("[data-testid='name-input-field']")
        error_message = page.locator("[data-testid='name-input-error']")
        next_button = page.locator("[data-testid='zhongkao-next-button']")
        
        # Clear and input the test value
        name_input.clear()
        name_input.fill(input_value)
        
        # Small wait for validation to process
        page.wait_for_timeout(100)
        
        if should_be_valid:
            # For valid input: no error message, Next button enabled
            expect(error_message).not_to_be_visible()
            expect(next_button).to_be_enabled()
        else:
            # For invalid input: error message shown, Next button disabled
            expect(error_message).to_be_visible()
            expected_error = COMMON_CONFIG['validation']['name'][error_key]
            expect(error_message).to_have_text(expected_error)
            expect(next_button).to_be_disabled()
        

        
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
        page_indicator_text = format_page_indicator(2, 3)
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
        page_indicator_text = format_page_indicator(1, 3)
        expect(page.locator(".zhongkao-page-indicator")).to_contain_text(page_indicator_text)
        
        # Verify name is still there
        name_input = page.locator(".zhongkao-input-field")
        expect(name_input).to_have_value("John")