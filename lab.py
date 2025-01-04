from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException

class LabQuestionnaire:

    URL = "https://bluejack.binus.ac.id/prk/auth/login"

    def __init__(self, driver: webdriver, credentials: dict[str, str], timeout: float=10.0):
        self.nim = credentials["NIM"]
        self.password = credentials["PASSWORD"]
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)
    
    def _load_page(self) -> None:
        self.driver.get(self.URL)
    
    def _login(self) -> None:
        self.wait.until(EC.title_contains('Login'))

        self.wait.until(
            EC.presence_of_element_located((By.NAME, 'username'))
        ).send_keys(self.nim)

        self.wait.until(
            EC.presence_of_element_located((By.NAME, 'password'))
        ).send_keys(self.password)

        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]"))
        ).click()

    def _fill_questionnaire(self) -> None:
        scores = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@value='4']")))
        for score in scores:
            score.click()

        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Save')]"))
        ).click()
        self.wait.until(EC.title_contains('Praktikum'))

    def start(self) -> bool:
        try:
            self._load_page()
            print("Logging in to your account.")
            self._login()
            print("Successfully logged in, taking questionnaire...")
            self._fill_questionnaire()
            print("Finished taking all questionnaire.")
            return True
        except Exception as e:
            # TODO: Better error handling
            print("An error occured: ", e)
            return False
        finally:
            self.driver.close()

if __name__ == '__main__':
    import json
    with open('config.json') as config_file:
        credentials = json.load(config_file)
    lab = LabQuestionnaire(webdriver.Chrome(), credentials)
    lab.start()
