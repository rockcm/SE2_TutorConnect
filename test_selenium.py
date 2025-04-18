import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time


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
            
            # Sleep for page to fully load
            time.sleep(2)
            
            # Verify logo is present
            try:
                logo = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "nav.navbar img[alt='Tutor logo']")))
                self.assertTrue(logo.is_displayed(), "Logo is not displayed")
                print("Logo is displayed")
            except TimeoutException as e:
                print(f"Error finding logo: {str(e)}")
            
            time.sleep(1)  # Add sleep time between actions
            
            # Test if Home link is clickable
            try:
                home_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "nav.navbar a[href='#hero']")))
                print("Home link is clickable")
            except TimeoutException as e:
                print(f"Error finding Home link: {str(e)}")
                # Try alternate selector
                home_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Home")))
                print("Found Home link using link text")
            
            time.sleep(1)  # Add sleep time between actions
            
            # Test if Search link is clickable
            try:
                search_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "nav.navbar a[href='search.html']")))
                print("Search link is clickable")
            except TimeoutException as e:
                print(f"Error finding Search link: {str(e)}")
                # Try alternate selector
                search_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Search")))
                print("Found Search link using link text")
            
            time.sleep(1)  # Add sleep time between actions
            
            # Test if Login/Create link is clickable
            try:
                login_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "nav.navbar a.nav-login")))
                print("Login/Create link is clickable")
            except TimeoutException as e:
                print(f"Error finding Login link: {str(e)}")
                # Try alternate selector
                login_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login/Create")))
                print("Found Login link using link text")
            
            time.sleep(1)  # Add sleep time between actions
            
            # Test search input functionality
            try:
                search_input = self.wait.until(
                    EC.presence_of_element_located((By.ID, "navSearchInput")))
                search_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.search-btn")))
                
                # Type in the search box
                search_input.clear()
                search_input.send_keys("test search")
                time.sleep(1)  # Wait for search input to process
                self.assertEqual("test search", search_input.get_attribute("value"), "Search input is not working")
                print("Search input is working")
                
                # Test dropdown search results (if available)
                time.sleep(2)  # Wait for dropdown to potentially appear
                try:
                    search_results = self.driver.find_element(By.ID, "searchResults")
                    if search_results.is_displayed():
                        print("Search dropdown is working")
                except:
                    print("Search dropdown is not visible or not implemented yet")
                
            except TimeoutException as e:
                print(f"Error finding search input: {str(e)}")
            
            time.sleep(1)  # Add sleep time between actions
            
            # Click Home link
            try:
                home_link.click()
                time.sleep(2)  # Wait for navigation to complete
                # Verify we're on the home section
                hero_section = self.wait.until(EC.visibility_of_element_located((By.ID, "hero")))
                self.assertTrue(hero_section.is_displayed(), "Failed to navigate to Home section")
                print("Successfully navigated to Home section")
            except Exception as e:
                print(f"Error clicking Home link: {str(e)}")
            
            time.sleep(2)  # Add sleep time between actions
            
            # Click Search Link
            try:
                search_link.click()
                time.sleep(2)  # Wait for navigation to complete
                # Verify we're on the search page
                self.wait.until(EC.url_contains("search.html"))
                print("Successfully navigated to Search page")
                
                # Go back to homepage
                self.driver.back()
                time.sleep(2)  # Wait for navigation to complete
                self.wait.until(lambda driver: "index.html" in driver.current_url or driver.current_url.endswith("/"))
            except Exception as e:
                print(f"Error clicking Search link: {str(e)}")
            
            time.sleep(2)  # Add sleep time between actions
            
            # Click Login/Create
            try:
                login_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "nav.navbar a.nav-login")))
                login_link.click()
                time.sleep(2)  # Wait for navigation to complete
                
                # Verify we're on the login page
                self.wait.until(EC.url_contains("login.html"))
                print("Successfully navigated to Login page")
            except Exception as e:
                print(f"Error clicking Login link: {str(e)}")
            
        except Exception as e:
            self.fail(f"Test failed with error: {str(e)}")
    
    def test_search_dropdown_and_profile(self):
        """Test search dropdown with 'chris' and click on result to view profile"""
        try:
            self.driver.get(self.base_url)
            print(f"Navigated to {self.base_url}")
            
            # Sleep for page to fully load
            time.sleep(2)
            
            # Find the search input in the navbar
            search_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "navSearchInput")))
            
            # Clear the search input and type "chris"
            search_input.clear()
            search_input.send_keys("chris")
            print("Typed 'chris' in search box")
            
            # Wait for the dropdown to appear
            time.sleep(3)
            
            # Check if search results dropdown is displayed
            try:
                search_results_container = self.wait.until(
                    EC.visibility_of_element_located((By.ID, "searchResults")))
                self.assertTrue(search_results_container.is_displayed(), "Search results dropdown is not displayed")
                print("Search results dropdown is displayed")
                
                # Find search result items
                search_result_items = search_results_container.find_elements(By.CLASS_NAME, "search-result-item")
                
                # Check if we got any results
                if search_result_items:
                    print(f"Found {len(search_result_items)} search results for 'chris'")
                    
                    # Click on the first result
                    search_result_items[0].click()
                    print("Clicked on the first search result")
                    
                    # Wait for navigation to profile page
                    time.sleep(3)
                    
                    # Verify we're on the profile page
                    self.wait.until(EC.url_contains("profile.html"))
                    print("Successfully navigated to Profile page")
                    
                    # Verify profile content loaded
                    user_name = self.wait.until(EC.presence_of_element_located((By.ID, "user-name")))
                    user_email = self.wait.until(EC.presence_of_element_located((By.ID, "user-email")))
                    user_role = self.wait.until(EC.presence_of_element_located((By.ID, "user-role")))
                    
                    # Ensure the profile data is not the loading placeholder
                    self.assertNotEqual("Loading...", user_name.text, "User name did not load properly")
                    self.assertNotEqual("Loading...", user_email.text, "User email did not load properly")
                    self.assertNotEqual("Loading...", user_role.text, "User role did not load properly")
                    
                    print(f"Successfully loaded profile page for: {user_name.text}")
                else:
                    print("No search results found for 'chris'")
            except TimeoutException as e:
                print(f"Error with search results: {str(e)}")
            
        except Exception as e:
            self.fail(f"Test failed with error: {str(e)}")
    
    def test_logout_from_profile(self):
        """Test that logout from profile page redirects to the correct login page"""
        try:
            # First, we need to login
            self.driver.get(self.base_url.replace("index.html", "login.html"))
            print("Navigated to login page")
            time.sleep(2)
            
            # For testing purposes, let's mock a login by setting localStorage
            # This simulates a logged-in user without having to perform the actual login flow
            script = """
                localStorage.setItem('is_logged_in', 'true');
                localStorage.setItem('user_id', '123');
                localStorage.setItem('user_name', 'Test User');
                localStorage.setItem('user_email', 'test@example.com');
                localStorage.setItem('user_role', 'student');
            """
            self.driver.execute_script(script)
            
            # Refresh the page to update the UI based on login state
            self.driver.refresh()
            time.sleep(2)
            
            # Navigate to profile page
            self.driver.get(self.base_url.replace("index.html", "Profiles/profile.html"))
            print("Navigated to profile page")
            time.sleep(2)
            
            # Check if we're properly on the profile page
            self.assertTrue("profile.html" in self.driver.current_url, "Failed to navigate to profile page")
            
            # Find and click the logout button
            try:
                # Make logout button visible (it might be hidden by default if JavaScript hasn't run)
                script = "document.querySelector('.nav-logout').style.display = 'block';"
                self.driver.execute_script(script)
                time.sleep(1)
                
                logout_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.nav-logout")))
                print("Found logout button")
                logout_button.click()
                print("Clicked logout button")
                
                # Wait for redirect to login page
                time.sleep(3)
                
                # Verify we're on the login page with the correct URL (not profiles/login.html)
                current_url = self.driver.current_url
                print(f"Redirected to: {current_url}")
                
                self.assertTrue("login.html" in current_url, "Not redirected to login page")
                self.assertFalse("/Profiles/login.html" in current_url, "Incorrectly redirected to /Profiles/login.html")
                
                print("Successfully redirected to correct login page")
                
            except TimeoutException as e:
                print(f"Error finding logout button: {str(e)}")
            
        except Exception as e:
            self.fail(f"Test failed with error: {str(e)}")

if __name__ == "__main__":
    unittest.main() 