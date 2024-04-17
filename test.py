from selenium import webdriver
import time

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

try:
    # Open the registration page
    driver.get("http://127.0.0.1:8000/register/")

    # Find the username, email, password, confirm password input fields, and submit button
    username_field = driver.find_element_by_id("id_username")
    email_field = driver.find_element_by_id("id_email")
    password_field = driver.find_element_by_id("id_password")
    confirm_password_field = driver.find_element_by_id("id_confirm_password")
    submit_button = driver.find_element_by_xpath("//input[@type='submit']")

    # Enter registration details
    username_field.send_keys("test_user")
    email_field.send_keys("test@example.com")
    password_field.send_keys("test_password")
    confirm_password_field.send_keys("test_password")

    # Click the submit button
    submit_button.click()

    # Wait for a few seconds to allow the page to load
    time.sleep(3)

    # Check if registration was successful by verifying the redirected URL
    if "loginpage" in driver.current_url:
        print("Registration successful! User redirected to login page.")
    else:
        print("Registration failed!")

finally:
    # Close the browser
    driver.quit()
