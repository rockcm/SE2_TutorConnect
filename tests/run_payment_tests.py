#!/usr/bin/env python3
"""
Payment Testing Script for TutorConnect

This script runs automated tests for the payment page functionality,
testing various Stripe test card scenarios.

Usage:
    python run_payment_tests.py
"""

import os
import sys
import argparse
from test_payment_page import run_tests

def main():
    parser = argparse.ArgumentParser(description="Run TutorConnect payment tests")
    parser.add_argument("--headless", action="store_true", help="Run tests in headless mode")
    args = parser.parse_args()
    
    # Set headless flag if specified
    if args.headless:
        os.environ["HEADLESS"] = "1"
    
    print("Starting TutorConnect payment tests...")
    
    # Run the tests
    run_tests()
    
    print("Payment tests completed!")

if __name__ == "__main__":
    main()