#!/usr/bin/env python3
"""
Visual Payment Testing for TutorConnect

This script runs automated tests for the payment page functionality visibly,
showing the browser automation on screen for demonstration purposes.

Usage:
    python visual_payment_test.py
"""

import sys
import time
import os
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import threading
import subprocess
import atexit

# Add parent directory to path so we can import from server.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import the Flask app
try:
    from server import app
except ImportError:
    print("Could not import Flask app. Running in standalone mode.")
    app = None

# Test card data
TEST_CARDS = [
    {
        "name": "Successful Payment",
        "number": "4242424242424242",
        "expected_result": "Payment Successful!"
    },
    {
        "name": "Authentication Required",
        "number": "4000002500003155",
        "expected_result": "3D Secure authentication required"
    },
    {
        "name": "Insufficient Funds",
        "number": "4000000000009995",
        "expected_result": "Payment Failed"
    },
    {
        "name": "Expired Card",
        "number": "4000000000000069",
        "expected_result": "Payment Failed"
    }
]

class PaymentTest:
    def __init__(self, server_url=None, slow_mode=False):
        self.server_url = server_url or "http://localhost:5000"
        self.slow_mode = slow_mode
        self.server_process = None
        self.driver = None
        
    def start_server(self):
        """Start the Flask server if not running externally"""
        if app is not None:
            print("Starting Flask server...")
            def run_flask():
                app.run(port=5000)
            
            self.flask_thread = threading.Thread(target=run_flask)
            self.flask_thread.daemon = True
            self.flask_thread.start()
            time.sleep(1)
        else:
            # Try to start the server using subprocess
            try:
                print("Starting Flask server using subprocess...")
                self.server_process = subprocess.Popen(
                    ["python3", "server.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                time.sleep(3)  # Give server time to start
            except Exception as e:
                print(f"Failed to start server: {e}")
                print("Please start the server manually before running tests.")
                return False
        
        return True
    
    def setup_driver(self):
        """Set up the Chrome WebDriver"""
        try:
            print("Setting up Chrome WebDriver...")
            chrome_options = Options()
            # Don't use headless mode so we can see the browser
            # chrome_options.add_argument("--start-maximized")
            
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            
            # Make the browser window a nice size for demo
            self.driver.set_window_size(1024, 768)
            
            return True
        except Exception as e:
            print(f"Failed to set up WebDriver: {e}")
            print("\nTroubleshooting tips:")
            print("1. Make sure Chrome browser is installed")
            print("2. Try installing ChromeDriver manually: https://chromedriver.chromium.org/")
            print("3. For WSL/Linux, you might need to install Chrome using:")
            print("   wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
            print("   sudo apt install ./google-chrome-stable_current_amd64.deb")
            return False
    
    def slow_send_keys(self, element, text):
        """Send keys to element with a delay for visual effect"""
        for char in text:
            element.send_keys(char)
            if self.slow_mode:
                time.sleep(0.1)
            else:
                time.sleep(0.05)
    
    def test_payment_card(self, card_data):
        """Test a specific payment card"""
        print(f"\nTesting {card_data['name']} card: {card_data['number']}")
        
        try:
            # Navigate to the payment page
            self.driver.get(f"{self.server_url}/payment")
            
            # Wait for the page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "card-element"))
            )
            
            # Add a pause so we can see the page
            print("  Viewing payment page...")
            time.sleep(1 if self.slow_mode else 0.5)
            
            # Switch to the Stripe iframe
            stripe_iframe = self.driver.find_element(By.CSS_SELECTOR, "iframe[src^='https://js.stripe.com']")
            self.driver.switch_to.frame(stripe_iframe)
            
            # Wait for the card number field
            card_number_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[placeholder='Card number']"))
            )
            
            # Fill in the card details
            print("  Entering card number...")
            self.slow_send_keys(card_number_input, card_data["number"])
            
            print("  Entering expiration date...")
            expiry_input = self.driver.find_element(By.CSS_SELECTOR, "[placeholder='MM / YY']")
            self.slow_send_keys(expiry_input, "1225")
            
            print("  Entering CVC...")
            cvc_input = self.driver.find_element(By.CSS_SELECTOR, "[placeholder='CVC']")
            self.slow_send_keys(cvc_input, "123")
            
            print("  Entering ZIP code...")
            zip_input = self.driver.find_element(By.CSS_SELECTOR, "[placeholder='ZIP']")
            self.slow_send_keys(zip_input, "12345")
            
            # Switch back to the main content
            self.driver.switch_to.default_content()
            
            # Click the submit button
            print("  Submitting payment...")
            submit_button = self.driver.find_element(By.ID, "submit-button")
            submit_button.click()
            
            # Wait for the result
            time.sleep(3)  # Give time for the payment to process
            
            try:
                # Check for various outcomes
                message_element = self.driver.find_element(By.ID, "payment-message")
                message_text = message_element.text
                
                if card_data["expected_result"] in message_text:
                    print(f"  ✅ Test passed: {message_text}")
                else:
                    print(f"  ❌ Test failed: Expected '{card_data['expected_result']}' but got '{message_text}'")
                
                # For 3D Secure, we would need to handle the popup, but we'll just acknowledge it
                if "3D Secure" in message_text:
                    print("  Note: 3D Secure authentication would show a popup in a real test")
            
            except Exception as e:
                print(f"  ❌ Test failed: Could not verify result: {e}")
            
            # Pause to view the result
            wait_time = 5 if self.slow_mode else 3
            print(f"  Waiting {wait_time} seconds to view the result...")
            time.sleep(wait_time)
            
            return True
        except Exception as e:
            print(f"  ❌ Test failed with error: {e}")
            return False
    
    def run_tests(self):
        """Run tests for all test cards"""
        if not self.start_server():
            return False
        
        if not self.setup_driver():
            return False
        
        print("\n========== STARTING PAYMENT TESTS ==========")
        
        try:
            for card in TEST_CARDS:
                self.test_payment_card(card)
            
            print("\n========== PAYMENT TESTS COMPLETED ==========")
            print(f"Tested {len(TEST_CARDS)} different payment scenarios")
            return True
        
        except Exception as e:
            print(f"\n❌ Tests failed with error: {e}")
            return False
        
        finally:
            # Clean up
            if self.driver:
                print("\nClosing browser...")
                self.driver.quit()
            
            if self.server_process:
                print("Stopping server...")
                self.server_process.terminate()

def main():
    parser = argparse.ArgumentParser(description="Run visual payment tests for TutorConnect")
    parser.add_argument("--url", help="URL of the payment server if already running")
    parser.add_argument("--slow", action="store_true", help="Run in slow mode for better visualization")
    args = parser.parse_args()
    
    # Register cleanup for Ctrl+C
    def cleanup():
        print("\nCleaning up resources...")
    
    atexit.register(cleanup)
    
    # Run the tests
    tester = PaymentTest(server_url=args.url, slow_mode=args.slow)
    tester.run_tests()

if __name__ == "__main__":
    main()