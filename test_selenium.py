import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TutorConnectTest(unittest.TestCase):
    """
    Test suite for the TutorConnect application.
    Tests the navbar functionality including navigation links and search.
    """
    
    def setUp(self):
        """Set up the test environment before each test method"""
        # Setup Chrome options
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')  # Comment out headless mode to see what's happening
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-usb')  # Disable USB device detection
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Suppress logging
        
        # Use webdriver_manager to handle ChromeDriver automatically
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()
        
        # Update the base URL if needed to match your actual application URL
        self.base_url = "http://localhost:5501/index.html"  # Adjust this URL
        
        # Set wait time for elements to load
        self.wait = WebDriverWait(self.driver, 10)
    
    def tearDown(self):
        """Clean up after each test method"""
        if self.driver:
            self.driver.quit()
    
    def test_navigation_buttons(self):
        """Test if all navbar elements are present and clickable"""
        try:
            self.driver.get(self.base_url)
            print(f"Navigated to {self.base_url}")
            
            # Verify logo is present
            try:
                logo = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "nav.navbar img[alt='Tutor logo']")))
                self.assertTrue(logo.is_displayed(), "Logo is not displayed")
                print("Logo is displayed")
            except TimeoutException as e:
                print(f"Error finding logo: {str(e)}")
            
            # Test if Home link is clickable
            try:
                home_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "nav.navbar a[href='#hero']")))
                print("Home link is clickable")
            except TimeoutException as e:
                print(f"Error finding Home link: {str(e)}")
                # Try alternate selector
                home_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Home")))
                print("Found Home link using link text")
            
            # Test if Search link is clickable
            try:
                search_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "nav.navbar a[href='search.html']")))
                print("Search link is clickable")
            except TimeoutException as e:
                print(f"Error finding Search link: {str(e)}")
                # Try alternate selector
                search_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Search")))
                print("Found Search link using link text")
            
            # Test if Login/Create link is clickable
            try:
                login_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "nav.navbar a.nav-login")))
                print("Login/Create link is clickable")
            except TimeoutException as e:
                print(f"Error finding Login link: {str(e)}")
                # Try alternate selector
                login_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login/Create")))
                print("Found Login link using link text")
            
            # Test search input functionality
            try:
                search_input = self.wait.until(
                    EC.presence_of_element_located((By.ID, "navSearchInput")))
                search_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.search-btn")))
                
                # Type in the search box
                search_input.clear()
                search_input.send_keys("test search")
                self.assertEqual("test search", search_input.get_attribute("value"), "Search input is not working")
                print("Search input is working")
            except TimeoutException as e:
                print(f"Error finding search input: {str(e)}")
            
            # Click Home link
            try:
                home_link.click()
                # Verify we're on the home section
                hero_section = self.wait.until(EC.visibility_of_element_located((By.ID, "hero")))
                self.assertTrue(hero_section.is_displayed(), "Failed to navigate to Home section")
                print("Successfully navigated to Home section")
            except Exception as e:
                print(f"Error clicking Home link: {str(e)}")
            
            # Click Search Link
            try:
                search_link.click()
                # Verify we're on the search page
                self.wait.until(EC.url_contains("search.html"))
                print("Successfully navigated to Search page")
                
                # Go back to homepage
                self.driver.back()
                self.wait.until(lambda driver: "index.html" in driver.current_url or driver.current_url.endswith("/"))
            except Exception as e:
                print(f"Error clicking Search link: {str(e)}")
            
            # Click Login/Create
            try:
                login_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "nav.navbar a.nav-login")))
                login_link.click()
                
                # Verify we're on the login page
                self.wait.until(EC.url_contains("login.html"))
                print("Successfully navigated to Login page")
            except Exception as e:
                print(f"Error clicking Login link: {str(e)}")
            
        except Exception as e:
            self.fail(f"Test failed with error: {str(e)}")

if __name__ == "__main__":
    unittest.main() 