from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Constants
USERNAME = 'asederado1@gmail.com'
PASSWORD = 'mauzz123'
CAPTCHA_IFRAME_XPATH = "//iframe[@id='captcha-internal']"
BUTTON_XPATH = "//button[contains(@id, 'ember') and contains(@class, 'artdeco-button artdeco-button--muted artdeco-button--4 artdeco-button--tertiary ember-view social-actions-button react-button__trigger')]"
BUTTON_ACTUALIZAR_XPATH = "//div/main/div[4]/div/div[2]/div/button"

def scroll_to_bottom():
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    find_and_click_button(BUTTON_ACTUALIZAR_XPATH)
    
def scroll_to_bottom_more_posts():
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.3)
    more_posts_button = browser.find_element(By.XPATH, "//div[contains(@class, 'text-align-center')]/button[contains(@class, 'artdeco-button')]")
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", more_posts_button)
    time.sleep(0.2)
    browser.execute_script("arguments[0].click();", more_posts_button)
    print('more posts')
        

def find_and_click_button(xpath):
    try:
        button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        if button.is_enabled() and button.is_displayed():
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            if xpath is BUTTON_ACTUALIZAR_XPATH:
                print('actualizando')
            browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(0.2)
            browser.execute_script("arguments[0].click();", button)
            return True
        else:
            return False
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
        #get div with class text-align-center, with button inside with class artdeco-button artdeco-button--secondary mv5 t-14 t-black t-normal and click it
        #slide down
        scroll_to_bottom_more_posts()
        
        return True

def click_button(i, clicked_ids):
    try:
        button_id = i.get_attribute("id")
        if "react-button--active" in i.get_attribute("class") or button_id in clicked_ids:
            clicked_ids.append(button_id)
            return True
        else:
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, button_id)))
            browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", i)
            time.sleep(0.2)
            browser.execute_script("arguments[0].click();", i)
            clicked_ids.append(button_id)
            print('liked')
            return True
    except Exception as e:
        print(f"An exception occurred with the liking procedure: {str(e)}")
        return False

def get_buttons():
    return browser.find_elements(By.XPATH, BUTTON_XPATH)

# Script Starts Here

browser = webdriver.Chrome()
action = ActionChains(browser)

browser.get("https://www.linkedin.com")
browser.refresh()
time.sleep(2)
try:
    button = browser.find_element(By.CSS_SELECTOR, ".artdeco-global-alert-action.artdeco-button.artdeco-button--inverse.artdeco-button--2.artdeco-button--primary")
    button.click()
except:
    #reload page
    browser.refresh()
    pass
#clicked on button
time.sleep(2)
#a with data-tracking-control-name attribute value guest_homepage-basic_nav-header-signin
a = browser.find_element(By.CSS_SELECTOR, "a[data-tracking-control-name='guest_homepage-basic_nav-header-signin']")
a.click()
time.sleep(4)

# Handle Login Here
username = browser.find_element(By.XPATH, "//*[@id='username']")
password = browser.find_element(By.XPATH, "//*[@id='password']")

username.send_keys(USERNAME)
time.sleep(0.5)
password.send_keys(PASSWORD)
time.sleep(0.5)
sign_in = browser.find_element(By.XPATH, "//*[@id='organic-div']/form/div[3]/button")
sign_in.click()
time.sleep(4)

while browser.find_elements(By.XPATH, CAPTCHA_IFRAME_XPATH):
    time.sleep(2)
    print('Complete the captcha')

time.sleep(2)

browser.get("https://www.linkedin.com/feed/")
time.sleep(4)

while True:
    clicked_ids = []
    buttons = get_buttons()

    if len(buttons) == 0: 
        print("len 0")
        scroll_to_bottom()
        if not find_and_click_button(BUTTON_ACTUALIZAR_XPATH):
            print("error actualizando len 0")
            
            buttons = get_buttons()
            time.sleep(2)
            continue
    for i in buttons:
        if not click_button(i, clicked_ids):
            print("Skipping this button and moving to the next one...")
            scroll_to_bottom()
            if not find_and_click_button(BUTTON_ACTUALIZAR_XPATH):
                buttons = get_buttons()

                print("error")
                time.sleep(1)
                break
            time.sleep(1)
            print("like")
            continue

    scroll_to_bottom()
    time.sleep(2)