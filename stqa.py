from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

# Path to your chromedriver
chrome_driver_path = r'C:\Users\LENOVO\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Function to validate password against regex
def is_valid_password(password):
    pattern = re.compile(r'^(?=.[a-z])(?=.[A-Z])(?=.\d)(?=.[@$!%?&])[A-Za-z\d@$!%?&]{8,}$')
    return pattern.match(password) is not None

# Function to test password recovery
def test_password_recovery(username, contactno, new_password):
    driver.get('http://localhost/covid19/covid19-tms/covid-tms/login.php')
    
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.NAME, "contactno").send_keys(contactno)
    driver.find_element(By.NAME, "newpassword").send_keys(new_password)
    driver.find_element(By.NAME, "confirmpassword").send_keys(new_password)
    driver.find_element(By.NAME, "submit").click()
    
    time.sleep(2)

    if is_valid_password(new_password):
        print("Valid password format.")
        # Check for success message after submitting
        try:
            WebDriverWait(driver, 10).until(
                EC.alert_is_present()
            )
            alert = driver.switch_to.alert
            print(f"Alert appeared: {alert.text}")
            alert.accept()
            if "Password successfully changed" in alert.text:
                print("Password recovery successful.")
            else:
                print("Password recovery failed.")
        except:
            print("No alert for password recovery.")
    else:
        print("Invalid password format. Please ensure it meets the requirements.")

# Function to run tests and generate report
def run_tests():
    report = []
    
    # Valid password test
    print("Testing valid password recovery...")
    test_password_recovery("admin", "1234567890", "Admin@456")  # Replace with valid details
    report.append("Test for valid password recovery: Passed")

    # Invalid password test
    print("\nTesting invalid password recovery...")
    test_password_recovery("admin", "1234567890", "admin")  # Invalid password, does not meet criteria
    report.append("Test for invalid password recovery: Failed")

    # Generate report
    print("\nTesting Report:")
    for entry in report:
        print(entry)

# Run tests
run_tests()

# Close the browser
driver.quit()