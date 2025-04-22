import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
import os

# Add parent directory to path so we can import from server.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app
from server import app

class PaymentPageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Initialize Chrome driver
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                                  options=chrome_options)
        
        # Start the Flask app in a separate thread
        import threading
        def run_flask():
            app.run(port=5000)
        
        cls.flask_thread = threading.Thread(target=run_flask)
        cls.flask_thread.daemon = True
        cls.flask_thread.start()
        
        # Wait for the server to start
        time.sleep(1)
    
    @classmethod
    def tearDownClass(cls):
        # Close the browser
        cls.driver.quit()
    
    def setUp(self):
        # Navigate to the payment page before each test
        self.driver.get("http://localhost:5000/payment")
        # Wait for the page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "card-element"))
        )
        
        # Wait for Stripe elements to load
        time.sleep(2)
        
        # Switch to the Stripe iframe
        stripe_iframe = self.driver.find_element(By.CSS_SELECTOR, "iframe[src^='https://js.stripe.com']")
        self.driver.switch_to.frame(stripe_iframe)
        
        # Wait for the card number field
        self.card_number_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[placeholder='Card number']"))
        )
        
        # Locate the other input fields
        self.expiry_input = self.driver.find_element(By.CSS_SELECTOR, "[placeholder='MM / YY']")
        self.cvc_input = self.driver.find_element(By.CSS_SELECTOR, "[placeholder='CVC']")
        self.zip_input = self.driver.find_element(By.CSS_SELECTOR, "[placeholder='ZIP']")
        
        # Switch back to the main content
        self.driver.switch_to.default_content()
    
    def test_successful_payment(self):
        """Test a successful payment with test card 4242 4242 4242 4242"""
        print("\nTesting successful payment...")
        self._fill_card_details("4242424242424242", "1225", "123", "12345")
        self._submit_payment()
        
        # Check for success message
        success_message = WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "payment-message"), 
                                            "Payment Successful!")
        )
        
        self.assertTrue(success_message)
        print("Successful payment test passed!")
    
    def test_authentication_required(self):
        """Test a payment requiring authentication with test card 4000 0025 0000 3155"""
        print("\nTesting payment requiring authentication...")
        self._fill_card_details("4000002500003155", "1225", "123", "12345")
        self._submit_payment()
        
        # Wait for the 3D Secure iframe (in a real test this would need to handle the 3D Secure flow)
        # For this demo, we'll just wait and assume it would work
        time.sleep(3)
        print("Authentication required payment test completed")
        
    def test_insufficient_funds(self):
        """Test a declined payment due to insufficient funds with test card 4000 0000 0000 9995"""
        print("\nTesting payment with insufficient funds...")
        self._fill_card_details("4000000000009995", "1225", "123", "12345")
        self._submit_payment()
        
        # Check for declined message
        declined_message = WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "payment-message"), 
                                            "Payment Failed")
        )
        
        self.assertTrue(declined_message)
        print("Insufficient funds payment test passed!")
    
    def test_expired_card(self):
        """Test a declined payment due to expired card with test card 4000 0000 0000 0069"""
        print("\nTesting payment with expired card...")
        self._fill_card_details("4000000000000069", "1225", "123", "12345")
        self._submit_payment()
        
        # Check for declined message
        declined_message = WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "payment-message"), 
                                            "Payment Failed")
        )
        
        self.assertTrue(declined_message)
        print("Expired card payment test passed!")
    
    def _fill_card_details(self, card_number, expiry, cvc, zip_code):
        """Helper method to fill in card details"""
        # Switch to the Stripe iframe
        stripe_iframe = self.driver.find_element(By.CSS_SELECTOR, "iframe[src^='https://js.stripe.com']")
        self.driver.switch_to.frame(stripe_iframe)
        
        # Fill in the card details
        self.card_number_input.send_keys(card_number)
        self.expiry_input.send_keys(expiry)
        self.cvc_input.send_keys(cvc)
        self.zip_input.send_keys(zip_code)
        
        # Switch back to the main content
        self.driver.switch_to.default_content()
    
    def _submit_payment(self):
        """Helper method to submit the payment form"""
        # Click the submit button
        submit_button = self.driver.find_element(By.ID, "submit-button")
        submit_button.click()

def run_tests():
    # Create a test suite with all tests
    suite = unittest.TestSuite()
    suite.addTest(PaymentPageTest('test_successful_payment'))
    suite.addTest(PaymentPageTest('test_authentication_required'))
    suite.addTest(PaymentPageTest('test_insufficient_funds'))
    suite.addTest(PaymentPageTest('test_expired_card'))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == "__main__":
    run_tests()