from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def get_vin():
    vin = 'WBAVM1C51FV498337'
    return vin

def solve_captcha():
    pass

def get_pdf(vin):
    driver = webdriver.Chrome(executable_path='/home/yn/Documents/chromedriver')
    driver.get(url)
    vin_form = driver.find_element(By.NAME, "vin")
    vin_form.send_keys(vin)
    capture_path = '/home/yn/Documents/screen.png'
    vin_form.send_keys(Keys.ENTER)
    driver.save_screenshot(capture_path)

def change_pdf():
    pass

def main():
    vin = get_vin()
    print(vin)
    get_pdf(vin)

url = "https://bimmer.work"

if __name__ == '__main__':
    main()

