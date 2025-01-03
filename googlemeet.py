from __future__ import print_function

from google.auth.transport.requests import Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import subprocess


def run_browser():
    
    
    command = ['chrome.exe', '--remote-debugging-port=1005', '--user-data-dir=C:\\chrome\\1005']
    
    subprocess.Popen(command)
    
    #     print("Batch file executed successfully.")
    # except subprocess.TimeoutExpired:
    #     print("Batch file timed out.")
    # except subprocess.CalledProcessError as e:
    #     print(f"Batch file failed with error: {e}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")

def google_join(meeting_link,isOrganizer,username):
    run_browser()
    chrome_options = Options()
    chrome_options.debugger_address = "127.0.0.1:1005"
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.get(meeting_link)
    if isOrganizer == True:
        join_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, "//button[contains(@class, 'UywwFc-LgbsSe') and contains(@class, 'q9a6Xc')]"
            ))
        )

# Click the button
        join_button.click()
    if isOrganizer == False:
        try:
            # Attempt to find and click the "Join now" button
            join_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH, "//button[contains(@class, 'UywwFc-LgbsSe') and contains(@class, 'q9a6Xc')]"
                ))
            )

    # Click the button
            join_button.click()
        except Exception:
            try:
                ask_to_join_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((
                        By.XPATH, "//button[@jsname='Qx7uuf' and contains(@class, 'UywwFc-LgbsSe')]"
                    ))
                )

                # Click the button
                ask_to_join_button.click()
            except Exception:
                print("Neither 'Join now' nor 'Ask to join' button was found.")
        
def zoom_join(meeting_link,isOrganizer,username):
    run_browser()
    chrome_options = Options()
    chrome_options.debugger_address = "127.0.0.1:1005"
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
  
    driver.get(meeting_link)

    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @tabindex='0']")))

    element.click()


    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="zoom-ui-frame"]/div[2]/div/div[2]/h3[2]/span/a""")))


    element.click()

    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "webclient")))  # You can also use class or src
    driver.switch_to.frame(iframe)
    # if isOrganizer == True:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "input-for-name"))
    )
    element.send_keys(username)
    
    join_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and contains(@class, 'preview-join-button')]"))
    )

    # Click the button
    join_button.click()
