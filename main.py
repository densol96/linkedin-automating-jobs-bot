from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from getpass import getpass
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_driver_path = ChromeDriverManager().install()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(15)
while True:
    try:
        driver.get("https://www.linkedin.com/")
        email_entry = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#session_key"))
            )
        password_entry = driver.find_element(By.CSS_SELECTOR, "#session_password")
        button = driver.find_element(By.CSS_SELECTOR, "button[data-id='sign-in-form__submit-btn'].btn-md")
    except:
        pass
    else:
        break
# # while True:
# #     email = input("Please provide your email: ")
# #     password = getpass("Please provide your password: ")
# #     hidden_password = ""
# #     for i, letter in enumerate(password):
# #         if i == len(password)-1 or i==0:
# #             hidden_password += letter
# #         else:
# #             hidden_password += "*"

# #     confirm = input(f"""E-mail: {email}
# # Password: {hidden_password} ({len(password)} characters)
# # \nAre these credentials correct (yes/no) ? 
# # """)[0].lower()
# #     if confirm == "y":
# #         break

email = "deniss11sol@gmail.com"
password="Majkisi-2021!!"
while True:
    try:
        email_entry.send_keys(email)
        password_entry.send_keys(password)
        button.click()
    except:
         pass
    else:
         break

# # job_description = input("Provide your key-search for your dream job:")
job_description = "Java Junior"
search = driver.find_element(By.CSS_SELECTOR, "input.search-global-typeahead__input").send_keys(job_description + Keys.ENTER)

all_jobs = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "See all job results"))
).click()
time.sleep(2)
temp_jobs = driver.find_elements(By.CSS_SELECTOR, "ul.scaffold-layout__list-container  li.jobs-search-results__list-item")

for scrolling_interval in range(0, len(temp_jobs), 2):
    driver.execute_script("arguments[0].scrollIntoView();", temp_jobs[scrolling_interval])

time.sleep(2)
jobs = driver.find_elements(By.CSS_SELECTOR, "ul.scaffold-layout__list-container  li.jobs-search-results__list-item a")
pagination_buttons = driver.find_elements(By.CSS_SELECTOR, ".artdeco-pagination__pages button")

print(f"Len: {pagination_buttons}")

href_links = []
print("hellos!")
num_pages = len(pagination_buttons)
print(num_pages)
for i in range(1, num_pages+1):
    if i != 1:
        time.sleep(5)
        temp_jobs = driver.find_elements(By.CSS_SELECTOR, "ul.scaffold-layout__list-container  li.jobs-search-results__list-item")
        for scrolling_interval in range(0, len(temp_jobs), 2):
            driver.execute_script("arguments[0].scrollIntoView();", temp_jobs[scrolling_interval])

        time.sleep(2)
        jobs = driver.find_elements(By.CSS_SELECTOR, "ul.scaffold-layout__list-container  li.jobs-search-results__list-item a")
        print(len(jobs))

    for job in jobs:
        if ("senior" not in job.text) and ("Senior" not in job.text):
            job.click()
            time.sleep(2)
            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.jobs-save-button'))
            ).click()
            time.sleep(2)
            follow_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.follow"))
            ).click()
    if i == num_pages:
        print(i, num_pages)
        break      
    time.sleep(3)     
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"button[aria-label='Page {i+1}']")))
    element.click()

while False:
    if i != 1:
        time.sleep(5)
        temp_jobs = driver.find_elements(By.CSS_SELECTOR, "ul.scaffold-layout__list-container  li.jobs-search-results__list-item")
        for scrolling_interval in range(0, len(temp_jobs), 2):
            driver.execute_script("arguments[0].scrollIntoView();", temp_jobs[scrolling_interval])

        time.sleep(2)
        jobs = driver.find_elements(By.CSS_SELECTOR, "ul.scaffold-layout__list-container  li.jobs-search-results__list-item a")
        print(len(jobs))

    for job in jobs:
        if ("senior" not in job.text) and ("Senior" not in job.text):
            job.click()
            time.sleep(2)
            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.jobs-save-button'))
            ).click()
            time.sleep(2)
            follow_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.follow"))
            ).click()
                
                    
    i+=1
    if len(pagination_buttons) != 0:
        pagination_buttons[0].click()
        time.sleep(1)
        pagination_buttons.pop(0)
        time.sleep(5)
    else:
        break

print(f"{i} pages scrapped..")


# for i in range(0, len(jobs)):
#     if "senior" not in jobs[i].text:
#         jobs_clicks[i].click()
#         save_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, '.jobs-save-button'))
#         ).click()
#         save_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, "button.follow"))
#         ).click()
        

# print(jobs[0].get_attribute("textContent"))


# follow_button = WebDriver(driver, 15).until(
#     EC.element_to_be_clickable((By.CSS_SELECTOR, "button.follow"))
# )
# follow_button.click()

