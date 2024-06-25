# Auto Get Public IP - ZTEF609 ( Indihome )

A Python script to automate the process of changing the WAN authentication type on an Indihome ZTEF609 router. The script changes the authentication type from Auto to PAP and back to Auto to reset the IP address, checking if the IP is public or private. If the IP is private, the script will repeat the process until a public IP is obtained, without restarting the router or disrupting the connection.

## Features

- Automates login to the Indihome ZTEF609 router.
- Changes WAN authentication type from Auto to PAP and back to Auto.
- Checks if the obtained IP is public or private.
- Repeats the process until a public IP is obtained.

## Requirements

- Python 3.x
- Selenium
- ChromeDriver
- Google Chrome

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/itsreezky/AutoGetPublicIP-ZTEF609.git
    cd AutoGetPublicIP-ZTEF609
    ```

2. Install the required Python packages:

    ```sh
    pip install selenium
    ```

3. Download ChromeDriver and ensure it matches your installed version of Google Chrome. Place the `chromedriver` executable in the path specified in the script or update the `driver_path` variable in the script to match your ChromeDriver location.

## Configuration

Update the following configuration variables in the script:

- `router_ip`: The IP address of your router (default is `http://192.168.1.1`).
- `username`: The username for logging into the router.
- `password`: The password for logging into the router.
- `driver_path`: The path to the ChromeDriver executable.

## Code Explanation

The script is organized into several functions to perform specific tasks:

### Importing Required Libraries

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
```

### Configuration

Update the configuration variables as needed:

```python
router_ip = 'http://192.168.1.1'
username = 'admin'
password = 'your_password'
driver_path = '/path/to/chromedriver'
```

### Initialize Browser

Set up the Selenium WebDriver:

```python
service = Service(driver_path)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 30)
```

### Function to Login to the Router

Logs into the router using the provided credentials:

```python
def login_to_router():
    try:
        driver.get(router_ip)
        wait.until(EC.presence_of_element_located((By.NAME, 'Username'))).send_keys(username)
        wait.until(EC.presence_of_element_located((By.NAME, 'Password'))).send_keys(password)
        wait.until(EC.element_to_be_clickable((By.ID, 'LoginId'))).click()
    except Exception as e:
        print(f"Error during login: {e}")
        driver.quit()
```

### Function to Change the WAN Authentication Type

Changes the WAN authentication type between 'Auto' and 'PAP':

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
        time.sleep(10)
    except Exception as e:
        print(f"Error during changing auth type: {e}")
        driver.quit()
```

### Function to Get the Public IP from the Router

Fetches the current public IP from the router's status page:

```python
def get_public_ip_from_router():
    try:
        wait.until(EC.element_to_be_clickable((By.ID, 'mmStatu'))).click()
        wait.until(EC.element_to_be_clickable((By.ID, 'smWanStatu'))).click()
        wait.until(EC.element_to_be_clickable((By.ID, 'ssmETHWANv46Conn'))).click()
        ip_element = wait.until(EC.presence_of_element_located((By.ID, 'wan_ip')))
        public_ip = ip_element.text.strip()
        return public_ip
    except Exception as e:
        print(f"Error during getting public IP: {e}")
        driver.quit()
```

### Function to Check if an IP is Private

Checks if the IP address is private:

```python
def is_private_ip(ip):
    private_ip_patterns = [
        re.compile(r'^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$'),
        re.compile(r'^172\.(1[6-9]|2[0-9]|3[0-1])\.\d{1,3}\.\d{1,3}$'),
        re.compile(r'^192\.168\.\d{1,3}\.\d{1,3}$')
    ]
    return any(pattern.match(ip) for pattern in private_ip_patterns)
```

### Main Logic

The main part of the script that uses the above functions to reset the IP:

```python
try:
    login_to_router()
    while True:
        current_ip = get_public_ip_from_router()
        print(f"Current IP: {current_ip}")
        if not is_private_ip(current_ip):
            print("Public IP obtained.")
            break
        change_auth_type('PAP')
        change_auth_type('Auto')
        time.sleep(30)
finally:
    driver.quit()
```

## Usage

1. Open a terminal and navigate to the directory containing the script.

2. Run the script:

    ```sh
    python change_ip.py
    ```

3. The script will log in to the router, change the WAN authentication type, and check the IP address. If the IP is private, it will repeat the process until a public IP is obtained.

## Troubleshooting

- Ensure that the ChromeDriver version matches your installed version of Google Chrome.
- Verify that the `driver_path` is correctly set to the location of your ChromeDriver executable.
- Make sure that the router's login page and elements IDs match those in the script. Adjust the script if your router's web interface has different element IDs or structure.

## Disclaimer

This script is provided as-is without any guarantees. Use it at your own risk. The author is not responsible for any damage or issues that may arise from using this script.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
