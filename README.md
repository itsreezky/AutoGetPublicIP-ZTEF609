# Automated Router Management Script Documentation

This documentation provides a detailed explanation of a Python script that uses Selenium to interact with a router's web interface to perform tasks such as logging in, changing WAN authentication types, and retrieving the public IP address. The script is designed to automate these tasks and can be modified to suit different routers by adjusting the element locators and credentials as needed.

## Prerequisites

- Python 3.x
- Selenium package
- ChromeDriver (matching your version of Chrome)
- Google Chrome browser

## Installation

1. Install the necessary Python package:
   ```sh
   pip install selenium
   ```

2. Download and install ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/). Ensure it matches your installed version of Google Chrome. Place the `chromedriver` executable in a known directory (e.g., `/home/reezky/chromedriver/chromedriver-linux64/`).

## Configuration

Before running the script, configure the following parameters:

- `router_ip`: The IP address of your router's web interface.
- `username`: Your router's username.
- `password`: Your router's password.
- `driver_path`: The path to your `chromedriver` executable.

## Script Overview

The script is divided into several functions, each responsible for a specific task:

### 1. Initialization

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuration
router_ip = 'http://192.168.1.1'
username = 'admin'
password = 'your_password'  # Replace with your router's username and password

# Initialize browser
driver_path = '/path/to/chromedriver'
service = Service(driver_path)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 30)
```

### 2. Login to Router

```python
def login_to_router():
    try:
        driver.get(router_ip)
        wait.until(EC.presence_of_element_located((By.NAME, 'Username'))).send_keys(username)
        wait.until(EC.presence_of_element_located((By.NAME, 'Password'))).send_keys(password)
        wait.until(EC.element_to_be_clickable((By.ID, 'LoginId'))).click()  # Adjust ID if different
    except Exception as e:
        print(f"Error during login: {e}")
        driver.quit()
```

### 3. Change WAN Authentication Type

```python
def change_auth_type(auth_type):
    try:
        wait.until(EC.element_to_be_clickable((By.ID, 'mmNet'))).click()
        wait.until(EC.element_to_be_clickable((By.ID, 'smWANConn'))).click()
        wait.until(EC.element_to_be_clickable((By.ID, 'ssmETHWAN46Con'))).click()

        wan_connection = wait.until(EC.presence_of_element_located((By.ID, 'Frm_WANCName0')))
        wan_connection.click()
        wan_connection.find_element(By.XPATH, "//option[@value='IGD.WD1.WCD1.WCPPP2']").click()

        auth_type_element = wait.until(EC.presence_of_element_located((By.ID, 'Frm_AuthType')))
        auth_type_element.click()
        auth_type_element.find_element(By.XPATH, f"//option[@value='{auth_type}']").click()

        wait.until(EC.element_to_be_clickable((By.ID, 'Btn_DoEdit'))).click()

        time.sleep(10)  # Wait for the changes to be applied
    except Exception as e:
        print(f"Error during changing auth type: {e}")
        driver.quit()
```

### 4. Get Public IP from Router

```python
def get_public_ip_from_router():
    try:
        wait.until(EC.element_to_be_clickable((By.ID, 'mmStatu'))).click()
        wait.until(EC.element_to_be_clickable((By.ID, 'smWanStatu'))).click()
        wait.until(EC.element_to_be_clickable((By.ID, 'ssmETHWANv46Conn'))).click()

        ip_element = wait.until(EC.presence_of_element_located((By.ID, 'wan_ip')))  # Adjust ID as needed
        public_ip = ip_element.text.strip()
        return public_ip
    except Exception as e:
        print(f"Error during getting public IP: {e}")
        driver.quit()
```

### 5. Main Execution

The main block of the script performs the following:

- Logs into the router.
- Retrieves the current public IP.
- Changes the WAN authentication type back and forth to trigger a public IP change.
- Prints the new public IP and verifies if it has changed.
- Repeats the process until the public IP changes, then exits.

```python
try:
    login_to_router()

    current_ip = get_public_ip_from_router()
    print(f"Current IP: {current_ip}")

    while True:
        change_auth_type('PAP')  # Change to PAP
        change_auth_type('Auto')  # Change back to Auto

        new_ip = get_public_ip_from_router()
        print(f"New IP: {new_ip}")

        if new_ip != current_ip:
            print("Public IP has changed.")
            break

        time.sleep(30)  # Wait a few seconds before trying again

finally:
    driver.quit()
```

## Notes

- Ensure the element locators (`By.ID`, `By.NAME`, `By.XPATH`, etc.) match the actual elements on your router's web interface. You may need to inspect your router's web pages and update the script accordingly.
- The script is designed to handle exceptions and close the browser in case of an error, ensuring that the session is properly terminated.
- Adjust the sleep durations as needed based on your router's response times.

## License

This script is provided "as is" without any warranty. Use it at your own risk and ensure you comply with any relevant terms of service or usage policies of your router.

## Author

This script was created by Reezky. Feel free to contribute and improve the script by submitting issues or pull requests on GitHub.
