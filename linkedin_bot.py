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


class LinkedInAutoBot:

    def __init__(self):
        chrome_driver_path = ChromeDriverManager().install()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        service = ChromeService(executable_path=chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(15)
        self.login(self.driver)
        print("Terminating the program... Bye!")

    def login(self, driver):
        # Open LinkedIn home-page, then continuously try to locate required fields untill they are present in the DOM
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
        # Enter and confirm your login details
        while True:
            email = input("Please provide your email: ")
            password = getpass("Please provide your password: ")
            hidden_password = ""
            # Display the masked password only showing the first and last character, the rest of the password is hidden with '*'
            for i, letter in enumerate(password):
                if i == len(password)-1 or i==0:
                    hidden_password += letter
                else:
                    hidden_password += "*"

            # Ask user to confirm their login details
            confirm = input(f"""
E-mail: {email}
Password: {hidden_password} ({len(password)} characters)
\nAre these credentials correct (yes/no) ? 
""")[0].lower()
            if confirm == "y":
                break
        # Send details and repeat this if something went wrong
        while True:
            try:
                email_entry.send_keys(email)
                password_entry.send_keys(password)
                button.click()
                time.sleep(3)
            except:
                pass
            else:
                break
         # Check if the login is succesfull. If not, try to log in again with new credentials
        if driver.current_url == "https://www.linkedin.com/uas/login-submit":
            self.login(driver)
        else:
            self.search(driver)
    
    def search(self, driver):
        while True:
            try:
                job_description = input("Provide your key-search for your dream job: ")
                search = driver.find_element(By.CSS_SELECTOR, "input.search-global-typeahead__input").send_keys(job_description + Keys.ENTER)

                all_jobs = WebDriverWait(driver, 15).until(
                            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "See all job results"))
                ).click()
                time.sleep(3)
            except:
                pass
            else:
                break
        self.apply_to_jobs(driver)
        
    def apply_to_jobs(self, driver):
        def scroll_down():
            time.sleep(2)
            temp_jobs = driver.find_elements(By.CSS_SELECTOR, "ul.scaffold-layout__list-container  li.jobs-search-results__list-item")
            # In order to make all buttons clickable, the driver needs to scroll to the very end of jobs' list 
            for scrolling_interval in range(0, len(temp_jobs), 2):
                driver.execute_script("arguments[0].scrollIntoView();", temp_jobs[scrolling_interval])
            time.sleep(2)
        scroll_down()

        # Now get the list of actual clickable buttons
        jobs = driver.find_elements(By.CSS_SELECTOR, "ul.scaffold-layout__list-container  li.jobs-search-results__list-item a")
        # Retrieve the number of pages for the all available jobs per search query
        num_pages = len(driver.find_elements(By.CSS_SELECTOR, ".artdeco-pagination__pages button"))

        for num_page in range(1, num_pages+1):
            if num_page != 1:
                # For every single page, other than the 1st one, the driver needs to repeat the same procedure of scrolling down and retrieving all the jobs that are present in the DOM
                scroll_down()
                jobs = driver.find_elements(By.CSS_SELECTOR, "ul.scaffold-layout__list-container  li.jobs-search-results__list-item a")
    
            for job in jobs:
                # Not interested in senior posts therefore exclude them
                if ("senior" not in job.text) and ("Senior" not in job.text):
                    time.sleep(3)
                    job.click()
                    save_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '.jobs-save-button'))
                    ).click()
                    follow_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.follow"))
                    ).click()
            # Check if the driver is on the last page. If it is -> there is no next page, therefore break out of the loop.        
            if num_page == num_pages:
                print(f"{num_page} / {num_pages} scraped! Task completed!")
                break
            # Otherwise, wait till the next button is present on the page and click on it, and repeat the loop      
            time.sleep(2)     
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"button[aria-label='Page {num_page+1}']")))
            element.click()

# Test the program
LinkedInAutoBot()