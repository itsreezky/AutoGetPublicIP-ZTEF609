from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuration
router_ip = 'http://192.168.1.1'
username = 'admin'
password = 'rizki21123'  # Replace with your router's username and password

# Initialize browser
driver_path = '/home/reezky/chromedriver/chromedriver-linux64/chromedriver'
service = Service(driver_path)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 30)

# Function to login to the router
def login_to_router():
    try:
        driver.get(router_ip)
        wait.until(EC.presence_of_element_located((By.NAME, 'Username'))).send_keys(username)
        wait.until(EC.presence_of_element_located((By.NAME, 'Password'))).send_keys(password)
        wait.until(EC.element_to_be_clickable((By.ID, 'LoginId'))).click()  # Login button, adjust if different
    except Exception as e:
        print(f"Error during login: {e}")
        driver.quit()

# Function to change the WAN authentication type
def change_auth_type(auth_type):
    try:
        # Navigate to Network -> WAN -> WAN Connection
        wait.until(EC.element_to_be_clickable((By.ID, 'mmNet'))).click()
        wait.until(EC.element_to_be_clickable((By.ID, 'smWANConn'))).click()
        wait.until(EC.element_to_be_clickable((By.ID, 'ssmETHWAN46Con'))).click()

        # Select the connection 'omci_ipv4_pppoe_1'
        wan_connection = wait.until(EC.presence_of_element_located((By.ID, 'Frm_WANCName0')))
        wan_connection.click()
        wan_connection.find_element(By.XPATH, "//option[@value='IGD.WD1.WCD1.WCPPP2']").click()

        # Change the authentication type
        auth_type_element = wait.until(EC.presence_of_element_located((By.ID, 'Frm_AuthType')))
        auth_type_element.click()
        auth_type_element.find_element(By.XPATH, f"//option[@value='{auth_type}']").click()

        # Click the Modify button
        wait.until(EC.element_to_be_clickable((By.ID, 'Btn_DoEdit'))).click()

        time.sleep(10)  # Wait for the changes to be applied
    except Exception as e:
        print(f"Error during changing auth type: {e}")
        driver.quit()

# Function to get the public IP from the router's status page
def get_public_ip_from_router():
    try:
        # Navigate to Status -> Network Interface -> WAN Connection
        wait.until(EC.element_to_be_clickable((By.ID, 'mmStatu'))).click()
        wait.until(EC.element_to_be_clickable((By.ID, 'smWanStatu'))).click()
        wait.until(EC.element_to_be_clickable((By.ID, 'ssmETHWANv46Conn'))).click()

        # Get the public IP
        ip_element = wait.until(EC.presence_of_element_located((By.ID, 'wan_ip')))  # Adjust ID as needed
        public_ip = ip_element.text.strip()
        return public_ip
    except Exception as e:
        print(f"Error during getting public IP: {e}")
        driver.quit()

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

