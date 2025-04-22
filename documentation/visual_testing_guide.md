# Visual Payment Testing Guide

This guide explains how to run the visual payment tests for TutorConnect, which demonstrate the Stripe payment functionality on screen.

## Prerequisites

To run the visual tests, you need:

1. Chrome browser installed on your machine
2. Python 3.6+ installed
3. The required dependencies:
   ```bash
   pip install -r tests/requirements_test.txt
   ```

## Running the Visual Tests

### Option 1: Terminal-based Simulation (No Browser Required)

The simplest way to demonstrate the payment functionality is through our terminal-based simulation:

```bash
python3 tests/payment_test_simulation.py
```

This will:
- Show a colorful, animated demonstration in your terminal
- Walk through each test card scenario step by step
- Display the expected outcomes for each payment attempt
- No browser or Chrome installation required

### Option 2: Visual Browser Automation (Chrome Required)

For a full visual demonstration that shows the actual payment page and browser interaction:

1. Make sure Chrome is installed on your system:
   
   **On Ubuntu/Debian:**
   ```bash
   wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
   sudo apt update
   sudo apt install ./google-chrome-stable_current_amd64.deb
   ```
   
   **On macOS:**
   ```bash
   brew install --cask google-chrome
   ```
   
   **On Windows:**
   Download and install from https://www.google.com/chrome/

2. Start the Flask server in one terminal:
   ```bash
   python3 server.py
   ```

3. Run the visual test in another terminal:
   ```bash
   python3 tests/visual_payment_test.py
   ```

For a slower, more dramatic demonstration (easier to follow):
```bash
python3 tests/visual_payment_test.py --slow
```

## What You'll See

The visual browser automation will:

1. Launch Chrome and navigate to the payment page
2. Type the test card numbers character by character (like a human would)
3. Fill in the expiration date, CVC, and ZIP code
4. Submit the payment and show the results
5. Proceed through all test scenarios:
   - Successful payment (4242 4242 4242 4242)
   - Authentication required (4000 0025 0000 3155)
   - Insufficient funds (4000 0000 0000 9995)
   - Expired card (4000 0000 0000 0069)

## Troubleshooting

If you encounter issues with Chrome:

1. Make sure Chrome is properly installed and accessible in your PATH
2. Try updating ChromeDriver: `pip install --upgrade webdriver-manager`
3. For WSL users, you may need X server forwarding to display Chrome (like VcXsrv on Windows)
4. As a fallback, use the terminal-based simulation which doesn't require Chrome

## For Presentations

- The slow mode (`--slow` flag) is perfect for presentations as it makes the typing and interactions more visible to an audience
- For demo environments where browser installation is problematic, use the terminal simulation
- If you need to skip certain scenarios, you can modify the `TEST_CARDS` list in the script