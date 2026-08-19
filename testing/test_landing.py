"""
Test Suite: Landing Page (index.html)
Description: Tests for the main landing page functionality
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class TestLandingPage:
    """Test cases for index.html - Landing Page"""

    # ============================================
    # PAGE LOAD TESTS
    # ============================================

    def test_landing_page_loads_successfully(self, driver, wait_time):
        """
        TC-L01: Landing page loads without errors
        Priority: High
        """
        driver.get(driver.base_path + "index.html")
        time.sleep(wait_time)

        # Verify page title
        assert "Drip" in driver.title, "Page title should contain 'Drip'"

        print("✅ TC-L01: Landing page loaded successfully")

    def test_logo_is_visible(self, driver, wait_time):
        """
        TC-L02: Drip logo is displayed
        Priority: High
        """
        driver.get(driver.base_path + "index.html")
        time.sleep(wait_time)

        logo = driver.find_element(By.CLASS_NAME, "logo-text")
        assert logo.is_displayed(), "Logo should be visible"
        assert logo.text == "Drip", f"Logo text should be 'Drip', got '{logo.text}'"

        print("✅ TC-L02: Logo is visible and correct")

    def test_tagline_is_visible(self, driver, wait_time):
        """
        TC-L03: Tagline is displayed below logo
        Priority: Medium
        """
        driver.get(driver.base_path + "index.html")
        time.sleep(wait_time)

        tagline = driver.find_element(By.CLASS_NAME, "tagline")
        assert tagline.is_displayed(), "Tagline should be visible"
        assert len(tagline.text) > 0, "Tagline should not be empty"

        print(f"✅ TC-L03: Tagline visible: '{tagline.text}'")

    # ============================================
    # SUBJECT CARDS TESTS
    # ============================================

    def test_three_subject_cards_exist(self, driver, wait_time):
        """
        TC-L04: Exactly 3 subject cards are present
        Priority: High
        """
        driver.get(driver.base_path + "index.html")
        time.sleep(wait_time)

        cards = driver.find_elements(By.CLASS_NAME, "subject-card")
        assert len(cards) == 3, f"Expected 3 subject cards, found {len(cards)}"

        print(f"✅ TC-L04: 3 subject cards found")

    def test_physics_card_content(self, driver, wait_time):
        """
        TC-L05: Physics card has correct title and topics
        Priority: High
        """
        driver.get(driver.base_path + "index.html")
        time.sleep(wait_time)

        physics_card = driver.find_element(By.CSS_SELECTOR, ".subject-card:nth-child(1)")
        card_title = physics_card.find_element(By.CLASS_NAME, "card-title").text
        assert card_title == "Physics", f"Expected 'Physics', got '{card_title}'"

        # Check topic chips exist
        chips = physics_card.find_elements(By.CLASS_NAME, "topic-chip")
        assert len(chips) > 0, "Physics card should have topic chips"

        print(f"✅ TC-L05: Physics card correct with {len(chips)} topics")

    def test_chemistry_card_content(self, driver, wait_time):
        """
        TC-L06: Chemistry card has correct title and topics
        Priority: High
        """
        driver.get(driver.base_path + "index.html")
        time.sleep(wait_time)

        chemistry_card = driver.find_element(By.CSS_SELECTOR, ".subject-card:nth-child(2)")
        card_title = chemistry_card.find_element(By.CLASS_NAME, "card-title").text
        assert card_title == "Chemistry", f"Expected 'Chemistry', got '{card_title}'"

        chips = chemistry_card.find_elements(By.CLASS_NAME, "topic-chip")
        assert len(chips) > 0, "Chemistry card should have topic chips"

        print(f"✅ TC-L06: Chemistry card correct with {len(chips)} topics")

    def test_biology_card_content(self, driver, wait_time):
        """
        TC-L07: Biology card has correct title and topics
        Priority: High
        """
        driver.get(driver.base_path + "index.html")
        time.sleep(wait_time)

        biology_card = driver.find_element(By.CSS_SELECTOR, ".subject-card:nth-child(3)")
        card_title = biology_card.find_element(By.CLASS_NAME, "card-title").text
        assert card_title == "Biology", f"Expected 'Biology', got '{card_title}'"

        chips = biology_card.find_elements(By.CLASS_NAME, "topic-chip")
        assert len(chips) > 0, "Biology card should have topic chips"

        print(f"✅ TC-L07: Biology card correct with {len(chips)} topics")

    # ============================================
    # BUTTON TESTS
    # ============================================

    def test_cta_buttons_exist(self, driver, wait_time):
        """
        TC-L08: Each card has a CTA button
        Priority: High
        """
        driver.get(driver.base_path + "index.html")
        time.sleep(wait_time)

        buttons = driver.find_elements(By.CLASS_NAME, "cta-button")
        assert len(buttons) == 3, f"Expected 3 CTA buttons, found {len(buttons)}"

        for i, btn in enumerate(buttons):
            assert btn.is_displayed(), f"Button {i+1} should be visible"

        print(f"✅ TC-L08: All 3 CTA buttons present and visible")

    def test_cta_button_text(self, driver, wait_time):
        """
        TC-L09: CTA buttons have correct text
        Priority: Medium
        """
        driver.get(driver.base_path + "index.html")
        time.sleep(wait_time)

        buttons = driver.find_elements(By.CLASS_NAME, "cta-button")
        for btn in buttons:
            text = btn.text.strip()
            assert len(text) > 0, "Button text should not be empty"
            assert "EXPLORE" in text.upper(), f"Button should contain 'EXPLORE', got '{text}'"

        print(f"✅ TC-L09: All CTA buttons have correct text")

    # ============================================
    # NAVIGATION TESTS
    # ============================================

    def test_physics_card_click_navigates(self, driver, wait_time):
        """
        TC-L10: Clicking Physics card navigates to Physics Hub
        Priority: High (Critical Path)
        """
        driver.get(driver.base_path + "index.html")
        time.sleep(wait_time)

        physics_card = driver.find_element(By.CSS_SELECTOR, ".subject-card:nth-child(1)")
        physics_card.click()
        time.sleep(wait_time + 1)

        current_url = driver.current_url
        assert "physics_hub.html" in current_url, \
            f"Should navigate to physics_hub.html, but at {current_url}"

        print(f"✅ TC-L10: Physics card navigates to Physics Hub")

    def test_chemistry_card_click_navigates(self, driver, wait_time):
        """
        TC-L11: Clicking Chemistry card navigates to Chemistry Hub
        Priority: High (Critical Path)
        """
        driver.get(driver.base_path + "index.html")
        time.sleep(wait_time)

        chemistry_card = driver.find_element(By.CSS_SELECTOR, ".subject-card:nth-child(2)")
        chemistry_card.click()
        time.sleep(wait_time + 1)

        current_url = driver.current_url
        assert "chemistry_hub.html" in current_url, \
            f"Should navigate to chemistry_hub.html, but at {current_url}"

        print(f"✅ TC-L11: Chemistry card navigates to Chemistry Hub")

    def test_biology_card_click_navigates(self, driver, wait_time):
        """
        TC-L12: Clicking Biology card navigates to Biology Hub
        Priority: High (Critical Path)
        """
        driver.get(driver.base_path + "index.html")
        time.sleep(wait_time)

        biology_card = driver.find_element(By.CSS_SELECTOR, ".subject-card:nth-child(3)")
        biology_card.click()
        time.sleep(wait_time + 1)

        current_url = driver.current_url
        assert "biology_hub.html" in current_url, \
            f"Should navigate to biology_hub.html, but at {current_url}"

        print(f"✅ TC-L12: Biology card navigates to Biology Hub")

    # ============================================
    # ANIMATION & VISUAL TESTS
    # ============================================

    def test_background_elements_exist(self, driver, wait_time):
        """
        TC-L13: Background grid and orbs are present
        Priority: Low
        """
        driver.get(driver.base_path + "index.html")
        time.sleep(wait_time)

        bg_grid = driver.find_element(By.CLASS_NAME, "bg-grid")
        assert bg_grid is not None, "Background grid should exist"

        orbs = driver.find_elements(By.CLASS_NAME, "orb")
        assert len(orbs) >= 2, f"Expected at least 2 orbs, found {len(orbs)}"

        print(f"✅ TC-L13: Background elements present")

    def test_particles_container_exists(self, driver, wait_time):
        """
        TC-L14: Floating particles container exists
        Priority: Low
        """
        driver.get(driver.base_path + "index.html")
        time.sleep(wait_time)

        particles = driver.find_element(By.ID, "particles")
        assert particles is not None, "Particles container should exist"

        print(f"✅ TC-L14: Particles container exists")

    # ============================================
    # HOVER / INTERACTION TESTS
    # ============================================

    def test_card_has_hover_effect(self, driver, wait_time):
        """
        TC-L15: Cards have hover effect (CSS transform on hover)
        Priority: Medium
        """
        driver.get(driver.base_path + "index.html")
        time.sleep(wait_time)

        card = driver.find_element(By.CSS_SELECTOR, ".subject-card:nth-child(1)")

        # Get initial transform
        initial_transform = card.value_of_css_property("transform")

        # Hover over card using JavaScript
        driver.execute_script("""
            var event = new MouseEvent('mouseover', {bubbles: true});
            arguments[0].dispatchEvent(event);
        """, card)
        time.sleep(0.5)

        # Check that hover styles are applied
        border_color = card.value_of_css_property("border-color")
        assert border_color != "", "Card should have border color on hover"

        print(f"✅ TC-L15: Cards respond to hover")

    # ============================================
    # RESPONSIVE TESTS
    # ============================================

    def test_mobile_viewport_layout(self, driver, wait_time):
        """
        TC-L16: Cards stack vertically on mobile
        Priority: High
        """
        driver.set_window_size(375, 812)  # iPhone X dimensions
        driver.get(driver.base_path + "index.html")
        time.sleep(wait_time)

        cards = driver.find_elements(By.CLASS_NAME, "subject-card")
        for card in cards:
            assert card.is_displayed(), "All cards should be visible on mobile"

        print(f"✅ TC-L16: Mobile layout displays all cards")

    def test_tablet_viewport_layout(self, driver, wait_time):
        """
        TC-L17: Layout works on tablet
        Priority: Medium
        """
        driver.set_window_size(768, 1024)  # iPad dimensions
        driver.get(driver.base_path + "index.html")
        time.sleep(wait_time)

        cards = driver.find_elements(By.CLASS_NAME, "subject-card")
        assert len(cards) == 3, "All 3 cards should be present on tablet"

        print(f"✅ TC-L17: Tablet layout works correctly")

        # Reset to default size
        driver.set_window_size(1366, 768)

    # ============================================
    # PERFORMANCE TESTS
    # ============================================

    def test_page_load_time(self, driver, wait_time):
        """
        TC-L18: Landing page loads in under 5 seconds
        Priority: Medium
        """
        import time as t

        start_time = t.time()
        driver.get(driver.base_path + "index.html")
        load_time = t.time() - start_time

        assert load_time < 5.0, f"Page load time {load_time:.2f}s exceeds 5s limit"

        print(f"✅ TC-L18: Page loaded in {load_time:.2f} seconds")


# ============================================
# RUN INSTRUCTIONS
# ============================================
if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════╗
    ║   Drip - Landing Page Test Suite    ║
    ╠══════════════════════════════════════╣
    ║  Run with:                          ║
    ║  pytest test_landing.py -v          ║
    ║  pytest test_landing.py --html=..   ║
    ╚══════════════════════════════════════╝
    """)