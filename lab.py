from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

NIM = "YOUR_NIM"
PASSWORD = "YOUR_PASSWORD"

URL = "https://bluejack.binus.ac.id/prk/auth/login"
driver = None

def main():
    driver.get(URL)

    WebDriverWait(driver, 10).until(EC.title_contains('Login'))

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'username'))
    ).send_keys(NIM)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'password'))
    ).send_keys(PASSWORD)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]"))
    ).click()

    try:
        WebDriverWait(driver, 10).until(EC.title_contains('Questionnaire'))
    except:
        raise Exception("No questionnaire available!")

    scores_in = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//input[@value='4']"))
    )

    for score in scores_in:
        score.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Save')]"))
    ).click()

if __name__ == '__main__':
    try:
        driver = webdriver.Chrome()
        main()
    except Exception as e:
        print(e)
    finally:
        driver.quit()
