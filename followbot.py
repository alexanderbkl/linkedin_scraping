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


#button_xpath is ul with class reusable-search__entity-result-list list-style-none, inside there is li, inside li there is a div, inside a div there is a div, inside div pick the third div, inside div there is a div, inside div there is a button
BUTTON_XPATH = "//main/div/div/div[1]/div/ul/li/div/div/div[3]/div/button"

BUTTON_ACTUALIZAR_XPATH = "/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/div[4]/div/div[2]/div/button"

def scroll_to_bottom():
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    #find_and_click_button(BUTTON_ACTUALIZAR_XPATH)

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
        #get button with class artdeco-button artdeco-button--secondary mv5 t-14 t-black t-normal and click it
        more_posts_button = browser.find_element(By.CSS_SELECTOR, ".artdeco-button.artdeco-button--secondary.mv5.t-14.t-black.t-normal")
        browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", more_posts_button)
        time.sleep(0.2)
        browser.execute_script("arguments[0].click();", more_posts_button)
        print('more posts')
        
        return False

def click_button(i, clicked_ids):
    try:
        button_id = i.get_attribute("id")
        if "react-button--active" in i.get_attribute("class") or button_id in clicked_ids:
            clicked_ids.append(button_id)
            return True
        else:
            browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", i)
            time.sleep(0.2)

            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, button_id)))
            time.sleep(0.2)
            browser.execute_script("arguments[0].click();", i)
            time.sleep(0.2)
            #send btn is button with aria-label Enviar ahora and inside there is a span with class artdeco-button__text
            send_btn = browser.find_element(By.XPATH, "//button[@aria-label='Enviar ahora']/span[@class='artdeco-button__text']")
            browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", send_btn)
            time.sleep(0.2)
            browser.execute_script("arguments[0].click();", send_btn)
            clicked_ids.append(button_id)
            print('liked')
            return True
    except Exception as e:
        print(f"An exception occurred with the liking procedure: {str(e)}")
        loop_count+=1
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

def next_page(page):
    try:
        #move browser to https://www.linkedin.com/search/results/people/?connectionOf=%5B%22ACoAAChwzx4Bi1JGknN8poTBkm89mxQd-b_nB1E%22%5D&network=%5B%22F%22%2C%22S%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH&page=NUMBER&sid=rcL
        #where NUMBER is the page number
        browser.get(f"https://www.linkedin.com/search/results/people/?connectionOf=%5B%22ACoAAChwzx4Bi1JGknN8poTBkm89mxQd-b_nB1E%22%5D&network=%5B%22F%22%2C%22S%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH&page={page}&sid=rcL")
        #page_btn = browser.find_element(By.XPATH, f"//button[@aria-label='Página {page}']")
        #browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", page_btn)
        time.sleep(2)
        #browser.execute_script("arguments[0].click();", page_btn)
        return True
    except Exception as e:
        print(f"An exception occurred with the next page procedure: {str(e)}")
        return False


while browser.find_elements(By.XPATH, CAPTCHA_IFRAME_XPATH):
    time.sleep(2)
    print('Complete the captcha')

time.sleep(2)

browser.get("https://www.linkedin.com/search/results/people/?connectionOf=%5B%22ACoAAChwzx4Bi1JGknN8poTBkm89mxQd-b_nB1E%22%5D&network=%5B%22F%22%2C%22S%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH&sid=Q~!")
time.sleep(4)
loop_count = 0

while True:
    loop_count += 1

    clicked_ids = []
    buttons = get_buttons()

    if len(buttons) == 0: 
        print("len 0")
        scroll_to_bottom()
        if not next_page(loop_count):
            print("error actualizando len 0 y loop count", loop_count)
            
            buttons = get_buttons()
            time.sleep(2)
            continue
    for i in buttons:
        #print button text
        time.sleep(1)
        #print(i.text)
        #if i.text == "Pendiente":
            #click on button with aria-label="Página n" where n is loop_count
        #    next_page(loop_count)
        #    break
        if not click_button(i, clicked_ids):
            print("Skipping this button and moving to the next one...")
            scroll_to_bottom()
            if not next_page(loop_count):
                buttons = get_buttons()

                print("error loop count", loop_count)
                time.sleep(1)
                break
            time.sleep(1)
            print("like")
            continue
    scroll_to_bottom()
    time.sleep(2)