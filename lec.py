from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class LecQuestionnaire:

    URL = "https://qmc.apps.binus.ac.id/survey_list?isMandatory=1"

    def __init__(self, driver: webdriver, credentials: dict[str, str], timeout: float=15.0):
        self.driver = driver
        self.email = credentials["EMAIL"]
        self.password = credentials["PASSWORD"]
        self.wait = WebDriverWait(self.driver, timeout)
    
    def _load_page(self) -> None:
        self.driver.get(self.URL)

    def _signin(self) -> None:
        # EMAIL
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
        ).send_keys(self.email)

        self.wait.until(
            EC.element_to_be_clickable((By.ID, 'idSIButton9'))
        ).click()

        sleep(1)

        # PASSWORD
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
        ).send_keys(self.password)

        self.wait.until(
            EC.element_to_be_clickable((By.ID, 'idSIButton9'))
        ).click()

        sleep(1)

        # SUBMIT
        self.wait.until(
            EC.element_to_be_clickable((By.ID, 'idSIButton9'))
        ).click()

    def _take_survey(self) -> bool:
        hasSurvey = False

        while True:
            try:
                # " Take Survey " btn
                self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-primary.btn-sm.w-100'))
                ).click()

                # " Start " btn
                self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.btn.btn-primary.btn-cons.btn-start'))
                ).click()

                scores = self.wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='radio'][id$='6']"))
                )

                for score in scores: # hidden element
                    self.driver.execute_script('arguments[0].click();', score)

                # " Done " btn
                self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='button-done']/button[contains(@class, 'btn-primary')]"))
                ).click()

                hasSurvey = True
                # redirected back to URL
            except:
                return hasSurvey
    
    def start(self) ->  bool:
        try:
            self._load_page()
            print("Signing in to your account.")
            self._signin()
            print("Successfully signed in, taking survey...")
            if not self._take_survey():
                print("Failed to load survey or none are available.")
                return False
            print("Finished taking all survey.")
            return True
        except Exception as e:
            # TODO: Better error handling
            print("An error occured: ", e)
            return False
        finally:
            self.driver.quit()

if __name__ == '__main__':
    import json
    with open('config.json') as config_file:
        credentials = json.load(config_file)
    lec = LecQuestionnaire(webdriver.Chrome(), credentials)
    lec.start()
