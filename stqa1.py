from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to your chromedriver
chrome_driver_path = r'C:\Users\LENOVO\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

def login(username, password):
    driver.get('http://localhost/covid19/covid19-tms/covid-tms/login.php')
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "inputpwd").send_keys(password)
    driver.find_element(By.XPATH, "//input[@name='login']").click()
    time.sleep(2)

def check_alert():
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"Alert appeared: {alert.text}")
        alert.accept()
        return True
    except:
        return False

def verify_login(success_expected):
    if success_expected:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Dashboard')]"))
            )
            print("Login successful with valid credentials")
        except Exception as e:
            print(f"Error: {e} - Login failed even though valid credentials were used.")
    else:
        if check_alert():
            print("Error message displayed for invalid login credentials.")
        else:
            error_message = "Invalid Details"  # Update this based on actual message in the page source
            if error_message in driver.page_source:
                print("Error message displayed for invalid login credentials.")
            else:
                print("Expected error message not found. Check the exact error message displayed on the page.")

# Run the tests
login("admin", "Admin@456")  # Replace with valid credentials
verify_login(success_expected=True)

login("user", "wrongpass")  # Replace with invalid credentials
verify_login(success_expected=False)

# Close the browser
driver.quit()