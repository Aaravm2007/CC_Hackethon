import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

def get_linkedin_profile_data(profile_url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    service = Service("chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)
        driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
        driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD)
        driver.find_element(By.ID, "password").submit()

        time.sleep(3)
        driver.get(profile_url)
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        name = soup.find("h1").text.strip() if soup.find("h1") else "Not found"
        job_title = soup.find("div", {"class": "text-body-medium"}).text.strip() if soup.find("div", {"class": "text-body-medium"}) else "Not found"

        skills = [tag.text.strip() for tag in soup.find_all("span", {"class": "mr1 hoverable-link-text"})]
        experience = [tag.text.strip() for tag in soup.find_all("span", {"class": "t-14 t-normal"})]

        return {"name": name, "job_title": job_title, "skills": skills, "experience": experience}
    
    finally:
        driver.quit()
