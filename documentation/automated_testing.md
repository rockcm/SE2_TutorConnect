# Automated Testing for TutorConnect

This document explains how to run the automated tests for the TutorConnect payment functionality.

## Payment Testing

The payment tests use Selenium to automate browser interactions and test different Stripe payment scenarios.

### Prerequisites

1. Install the required dependencies:

```bash
pip install -r tests/requirements_test.txt
```

2. Chrome browser installed (for Chrome WebDriver)

### Running the Tests

To run the payment tests:

```bash
python tests/run_payment_tests.py
```

This will:
1. Start the Flask server
2. Open a Chrome browser
3. Navigate to the payment page
4. Test multiple payment scenarios with different test cards
5. Report the results

### Headless Mode

To run tests without opening a visible browser window (useful for CI/CD):

```bash
python tests/run_payment_tests.py --headless
```

### Test Cases

The payment tests include the following scenarios:

1. **Successful Payment** - Tests a successful payment using the 4242 4242 4242 4242 test card
2. **Authentication Required** - Tests a payment requiring 3D Secure authentication using the 4000 0025 0000 3155 test card
3. **Insufficient Funds** - Tests a declined payment due to insufficient funds using the 4000 0000 0000 9995 test card
4. **Expired Card** - Tests a declined payment due to an expired card using the 4000 0000 0000 0069 test card

### Extending the Tests

To add more test cases:

1. Add new test methods to the `PaymentPageTest` class in `tests/test_payment_page.py`
2. Add the new test to the test suite in the `run_tests()` function

Example:

```python
def test_new_scenario(self):
    """Test a new payment scenario"""
    self._fill_card_details("4000000000000000", "1225", "123", "12345")
    self._submit_payment()
    # Add assertions here
```

Then add it to the test suite:

```python
suite.addTest(PaymentPageTest('test_new_scenario'))
```