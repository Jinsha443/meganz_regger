from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from pymailtm import MailTm
import names, time, random, string, uuid, threading

def password_gen(password=""):
    characters = string.ascii_letters + string.digits

    for _ in range(random.randint(12,18)):
        password = password + random.choice(characters)

    return password

def type_keys(obj, text):
    obj.click()
    time.sleep(0.5)
    for i in text:
        obj.send_keys(i)
        time.sleep(random.uniform(0.2, 0.111111))

def main(is_headless, id, save_file):
    options = webdriver.ChromeOptions()
    # options.binary_location = "/usr/bin/chromium"
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-audio-output")
    if is_headless:
        options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service("./chromedriver"), options=options)

    driver.get("https://mega.io/")
    time.sleep(1)
    driver.find_elements(by=By.CLASS_NAME, value="sign-up-btn")[0].click()
    time.sleep(1)

    while "bottom-pages" not in driver.find_element(value="bodyel").get_attribute(name="class"):
        pass

    try: acc = MailTm().get_account()
    except: 
        print("Lots of requests for temporary mail. Try to put fewer threads...")
        browsers.remove(id)
        driver.quit()
        return
    password = password_gen()

    errors = driver.find_elements(by=By.CLASS_NAME, value="error")
    type_keys(driver.find_element(value="register-firstname-registerpage2"), names.get_first_name())
    type_keys(driver.find_element(value="register-lastname-registerpage2"), names.get_last_name())
    type_keys(driver.find_element(value="register-email-registerpage2"), acc.address)
    type_keys(driver.find_element(value="register-password-registerpage2"), password)
    type_keys(driver.find_element(value="register-password-registerpage3"), password)

    for object in driver.find_elements(by=By.CLASS_NAME, value="understand-check"):
        try: object.find_element(by=By.CLASS_NAME, value="megaInputs").click()
        except: pass
    time.sleep(1)

    driver.find_element(value="register-check-registerpage2").click()
    driver.find_element(by=By.CLASS_NAME, value="register-button").click()

    if driver.find_elements(by=By.CLASS_NAME, value="error") != errors:
        browsers.remove(id)
        driver.quit()
        return

    try: driver.get(acc.wait_for_message().text.split()[22])
    except: 
        print("Lots of requests for temporary mail. Try to put fewer threads...")
        browsers.remove(id)
        driver.quit()
        return
    
    while "bottom-pages" not in driver.find_element(value="bodyel").get_attribute(name="class"):
        pass
    time.sleep(1)
    type_keys(driver.find_element(value="login-password2"), password)
    driver.find_element(by=By.CLASS_NAME, value="login-button").click()
    time.sleep(1)
    with open(save_file, "a") as file:
        file.write(f"{acc.address}:{password}\n")
    print(f"Browser({id}) has completed the work")
    browsers.remove(id)

global browsers
browsers = []

while True:
    try:
        threads = input("How many threads do you need?: ")
        if threads == "":
            threads = 1
        else:
            threads = int(threads)

        break
    except: print("again...")

is_headless = input("Will the browser be headless?(y/n): ").lower()
if is_headless == "n": is_headless = False
else: is_headless = True

save_file = input("File path to save(def: mega.txt): ")
if save_file == "": save_file = "mega.txt"

while True:
 for i in range(threads):
    id = str(uuid.uuid4())
    browsers.append(id)
    threading.Thread(target=main, args=(is_headless,id,save_file, )).start()
    while len(browsers) >= threads:
        time.sleep(1)