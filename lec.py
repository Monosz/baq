from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

EMAIL = "YOUR_EMAIL"
PASSWORD = "YOUR_PASSWORD"

URL = "https://qmc.apps.binus.ac.id/survey_list?isMandatory=1"
driver = webdriver.Chrome()

def signin() -> bool:
    try:
        # TODO: Check if already signed in (EdgeDriver)
        pass

    except:
        return True
    
    else:
        try:
            # EMAIL
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
            ).send_keys(EMAIL)

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'idSIButton9'))
            ).click()

            sleep(1)

            # PASSWORD
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
            ).send_keys(PASSWORD)

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'idSIButton9'))
            ).click()

            sleep(1)

            # SUBMIT
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'idSIButton9'))
            ).click()


        except Exception as e:
            print(e)
            return False
        
        else:
            return True

def take_survey() -> bool:
    hasSurvey = False;

    while True:
        try:
            # " Take Survey " btn
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-primary.btn-sm.w-100'))
            ).click()

            # " Start " btn
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.btn.btn-primary.btn-cons.btn-start'))
            ).click()

            score_ins = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='radio'][id$='6']"))
            )

            for score_in in score_ins: # hidden element
                driver.execute_script('arguments[0].click();', score_in)

            # " Done " btn
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='button-done']/button[contains(@class, 'btn-primary')]"))
            ).click()
            
            hasSurvey = True
            
            # redirected back to URL

        except:
            return hasSurvey

def main():
    try:
        driver.get(URL)

        if (signin()):
            print("Successfully signed in.")
        else:
            print("Failed to sign in.")
            return
        
        if (take_survey()):
            print("Finished taking survey.")
        else: 
            print("Failed to load survey or none are available.")
            return

    except Exception as e:
        print(e)

    finally:
        driver.close()

if __name__ == "__main__":
    main()
