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
        total_pages = ZHONGKAO_CONFIG['totalPages']

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
        page_indicator_text = format_page_indicator(2, total_pages)
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
        page_indicator_text = format_page_indicator(1, total_pages)
        expect(page.locator(".zhongkao-page-indicator")).to_contain_text(page_indicator_text)
        
        # Verify name is still there
        name_input = page.locator(".zhongkao-input-field")
        expect(name_input).to_have_value("John")


    def test_switch_between_manual_and_auto_generate_scores(self, page: Page):
        """
        Test that user can switch between manual input and auto-generated scores
        """
        # Step 1: Create test data - valid name and gender
        test_name = "张三"
        test_gender = ZHONGKAO_CONFIG['pages']['page2']['options'][0]  # "女"
        
        # Step 1: Create two lists of scores for the 10 courses
        manual_scores_set1 = ["100", "95", "88", "60", "45", "50", "16", "12", "16", "12"]
        manual_scores_set2 = ["90", "85", "92", "65", "48", "55", "20", "16", "12", "8"]
        
        total_pages = ZHONGKAO_CONFIG['totalPages']
        score_configs = ZHONGKAO_CONFIG['pages']['scorepage']['scores']
        
        # Navigate to the application
        page.goto("http://localhost:5173")
        page.click("[data-testid='nav-zhongkao']")
        expect(page.locator("[data-testid='zhongkao-title']")).to_have_text(ZHONGKAO_CONFIG['title'])
        
        # Enter name on page 1
        name_input = page.locator("[data-testid='name-input-field']")
        name_input.fill(test_name)
        page.click("[data-testid='zhongkao-next-button']")
        
        # Select gender on page 2
        gender_select = page.locator("[data-testid='dropdown-select']")
        gender_select.select_option(test_gender)
        page.click("[data-testid='zhongkao-next-button']")
        
        # Step 2: In page 3, choose manual input score and click next
        page_indicator = format_page_indicator(3, total_pages)
        expect(page.locator("[data-testid='zhongkao-page-indicator']")).to_contain_text(page_indicator)
        
        method_select = page.locator("[data-testid='dropdown-select']")
        method_select.select_option(ZHONGKAO_CONFIG['pages']['scoregenchoicepage']['options'][0])  # Manual input
        page.wait_for_timeout(200)
        page.click("[data-testid='zhongkao-next-button']")

        # Step 3: Input scores for each course using first set and click next
        page_indicator = format_page_indicator(4, total_pages)
        expect(page.locator("[data-testid='zhongkao-page-indicator']")).to_contain_text(page_indicator)
        
        score_inputs = page.locator("[data-testid='score-input-field']").all()
        dropdown_selects = page.locator("[data-testid='dropdown-select']").all()    
        
        # Fill in scores based on input type
        input_index = 0
        dropdown_index = 0
        for i, config in enumerate(score_configs):
            if len(config['range']) == 2:
                # Range input
                score_inputs[input_index].fill(manual_scores_set1[i])
                input_index += 1
            else:
                # Dropdown
                dropdown_selects[dropdown_index].select_option(manual_scores_set1[i])
                dropdown_index += 1
        
        page.wait_for_timeout(500)
        page.click("[data-testid='zhongkao-next-button']")

        # Step 4: In summary page, verify scores and total
        page_indicator = format_page_indicator(5, total_pages)
        expect(page.locator("[data-testid='zhongkao-page-indicator']")).to_contain_text(page_indicator)
        
        # Check each score value
        for i in range(len(score_configs)):
            score_locator = page.locator(f"[data-testid='summary-score-{i}'] .zhongkao-infobox-value")
            score_value = score_locator.inner_text().strip()
            assert score_value == manual_scores_set1[i], f"Score {i} mismatch: expected {manual_scores_set1[i]}, got {score_value}"
        
        # Check total score
        expected_total_1 = sum(int(score) for score in manual_scores_set1)
        total_score = page.locator("[data-testid='summary-total']").inner_text().strip()
        assert int(total_score) == expected_total_1, f"Total score mismatch: expected {expected_total_1}, got {total_score}"
        
        # Step 5: Click previous button twice to go back to page 3
        page.click("[data-testid='zhongkao-previous-button']")
        page.wait_for_timeout(300)
        page.click("[data-testid='zhongkao-previous-button']")
        page.wait_for_timeout(300)
        
        # Choose auto generated scores and click next
        page_indicator = format_page_indicator(3, total_pages)
        expect(page.locator("[data-testid='zhongkao-page-indicator']")).to_contain_text(page_indicator)
        
        method_select = page.locator("[data-testid='dropdown-select']")
        method_select.select_option(ZHONGKAO_CONFIG['pages']['scoregenchoicepage']['options'][1])  # Auto generate
        
        # Wait for scores to be generated
        page.wait_for_timeout(1000)
        page.click("[data-testid='zhongkao-next-button']")
        page.wait_for_timeout(500)
        
        # Step 6: In summary page, check valid scores and save total
        page_indicator = format_page_indicator(5, total_pages)
        expect(page.locator("[data-testid='zhongkao-page-indicator']")).to_contain_text(page_indicator)
        
        # Check each score is valid (not empty and within range)
        auto_scores_first = []
        for i, config in enumerate(score_configs):
            score_locator = page.locator(f"[data-testid='summary-score-{i}'] .zhongkao-infobox-value")
            score_value = score_locator.inner_text().strip()
            auto_scores_first.append(score_value)
            
            # Verify score is not empty
            assert score_value != '', f"Score {i} is empty"
            
            # Verify score is within valid range
            score_int = int(score_value)
            if len(config['range']) == 2:
                assert config['range'][0] <= score_int <= config['range'][1], \
                    f"Score {i} out of range: {score_int} not in [{config['range'][0]}, {config['range'][1]}]"
            else:
                assert score_int in config['range'], \
                    f"Score {i} not in valid options: {score_int} not in {config['range']}"
        
        # Save first auto-generated total score
        first_auto_total = int(page.locator("[data-testid='summary-total']").inner_text().strip())
        # Verify the total matches the sum of individual scores
        expected_first_total = sum(int(score) for score in auto_scores_first)
        assert first_auto_total == expected_first_total, \
            f"First auto-generated total mismatch: expected {expected_first_total}, got {first_auto_total}"
        
        # Step 7: Click previous button to go back to page 3, choose auto generated again
        page.click("[data-testid='zhongkao-previous-button']")
        page.wait_for_timeout(300)
        
        page_indicator = format_page_indicator(3, total_pages)
        expect(page.locator("[data-testid='zhongkao-page-indicator']")).to_contain_text(page_indicator)
        
        method_select = page.locator("[data-testid='dropdown-select']")
        method_select.select_option(ZHONGKAO_CONFIG['pages']['scoregenchoicepage']['options'][1])  # Auto generate again
        
        # Wait for scores to be generated
        page.wait_for_timeout(1000)
        page.click("[data-testid='zhongkao-next-button']")
        page.wait_for_timeout(500)
        
        # Step 8: In summary page, check valid scores and verify total
        page_indicator = format_page_indicator(5, total_pages)
        expect(page.locator("[data-testid='zhongkao-page-indicator']")).to_contain_text(page_indicator)
        
        # Check each score is valid
        auto_scores_second = []
        for i, config in enumerate(score_configs):
            score_locator = page.locator(f"[data-testid='summary-score-{i}'] .zhongkao-infobox-value")
            score_value = score_locator.inner_text().strip()
            auto_scores_second.append(score_value)
            
            # Verify score is not empty
            assert score_value != '', f"Score {i} is empty"
            
            # Verify score is within valid range
            score_int = int(score_value)
            if len(config['range']) == 2:
                assert config['range'][0] <= score_int <= config['range'][1], \
                    f"Score {i} out of range: {score_int} not in [{config['range'][0]}, {config['range'][1]}]"
            else:
                assert score_int in config['range'], \
                    f"Score {i} not in valid options: {score_int} not in {config['range']}"
        
        # Check if total score is different from first auto-generation
        second_auto_total = int(page.locator("[data-testid='summary-total']").inner_text().strip())
        
        # Note: In rare cases, they might be the same. We just expect it to be different when generating randomly twice:
        assert second_auto_total != first_auto_total, "Second auto-generated total is the same as first"

        # Verify the total matches the sum of individual scores
        expected_second_total = sum(int(score) for score in auto_scores_second)
        assert second_auto_total == expected_second_total, \
            f"Second auto-generated total mismatch: expected {expected_second_total}, got {second_auto_total}"
        
        # Step 9: Click previous button to go back to page 3, choose manual input
        page.click("[data-testid='zhongkao-previous-button']")
        page.wait_for_timeout(300)
        
        page_indicator = format_page_indicator(3, total_pages)
        expect(page.locator("[data-testid='zhongkao-page-indicator']")).to_contain_text(page_indicator)
        
        method_select = page.locator("[data-testid='dropdown-select']")
        method_select.select_option(ZHONGKAO_CONFIG['pages']['scoregenchoicepage']['options'][0])  # Manual input
        page.wait_for_timeout(200)
        page.click("[data-testid='zhongkao-next-button']")
        
        # Step 10: In page 4, check all fields are empty and total is 0
        page_indicator = format_page_indicator(4, total_pages)
        expect(page.locator("[data-testid='zhongkao-page-indicator']")).to_contain_text(page_indicator)
        
        # Verify all score inputs are empty
        score_inputs = page.locator("[data-testid='score-input-field']").all()
        for idx, score_input in enumerate(score_inputs):
            input_val = score_input.input_value()
            assert input_val == '', f"Score input {idx} should be empty, got '{input_val}'"
        
        # Verify total score is 0
        total_score_display = page.locator("[data-testid='total-score'] .zhongkao-total-value").inner_text().strip()
        assert int(total_score_display) == 0, f"Total score should be 0, got {total_score_display}"
        
        # Input scores using second set
        score_inputs = page.locator("[data-testid='score-input-field']").all()
        dropdown_selects = page.locator("[data-testid='dropdown-select']").all()
        
        input_index = 0
        dropdown_index = 0
        for i, config in enumerate(score_configs):
            if len(config['range']) == 2:
                score_inputs[input_index].fill(manual_scores_set2[i])
                input_index += 1
            else:
                dropdown_selects[dropdown_index].select_option(manual_scores_set2[i])
                dropdown_index += 1
        
        page.wait_for_timeout(500)
        page.click("[data-testid='zhongkao-next-button']")
        
        # Step 11: In summary page, verify scores and total match second set
        page_indicator = format_page_indicator(5, total_pages)
        expect(page.locator("[data-testid='zhongkao-page-indicator']")).to_contain_text(page_indicator)
        
        # Check each score value matches second set
        for i in range(len(score_configs)):
            score_locator = page.locator(f"[data-testid='summary-score-{i}'] .zhongkao-infobox-value")
            score_value = score_locator.inner_text().strip()
            assert score_value == manual_scores_set2[i], \
                f"Score {i} mismatch: expected {manual_scores_set2[i]}, got {score_value}"
        
        # Check total score matches second set
        expected_total_2 = sum(int(score) for score in manual_scores_set2)
        total_score = page.locator("[data-testid='summary-total']").inner_text().strip()
        assert int(total_score) == expected_total_2, \
            f"Total score mismatch: expected {expected_total_2}, got {total_score}"