from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium import webdriver
import time
try:

# Initialize Chrome WebDriver
    driver = webdriver.Chrome()
    print("WebDriver initialized.")

    # Open the desired URL
    driver.get("http://127.0.0.1:8000/about/")
    print("Website has been opened.")

    # Allow some time for the page to load
    time.sleep(3)

    # Check if specific elements are present
    header = driver.find_element(By.TAG_NAME, 'h1')
    print("Page Title Found: ", header.text)

    # Optionally, check if the text includes expected words
    assert "About Us" in header.text
    print("The 'About' page loaded correctly with the right header.")

except Exception as error:
    print("An error occurred:", str(error))
finally:
    # Close the browser
    driver.quit()
    print("Browser closed.")
