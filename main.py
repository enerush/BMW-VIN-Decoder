from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from anticaptchaofficial.recaptchav2proxyless import *

def get_vin():
    vin = 'WBAVM1C51FV498337'
    return vin

def solve_captcha(url, sitekey):
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key('7a0556a0ad5a2051060b0c45cd0d0740')
    solver.set_website_url(url)
    solver.set_website_key(sitekey)

    g_response = solver.solve_and_return_solution()
    if g_response != 0:
        print('g-response: ' + g_response)
    else:
        print('task finished with error ' + solver.error_code)


def get_pdf(vin):
    vin_form = driver.find_element(By.NAME, "vin")
    vin_form.send_keys(vin)
    vin_form.send_keys(Keys.ENTER)
    driver.save_screenshot(capture_path)

def change_pdf():
    pass

def main():
    url = "https://bimmer.work"
    vin = get_vin()

    driver = webdriver.Chrome(executable_path='/home/yn/Documents/chromedriver')
    page = driver.get(url)

    sitekey = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/form/div[3]/div').get_attribute('outerHTML')
    sitekey_clean = sitekey.split('"><div style="width:')[0].split('data-sitekey="')[-1]
    print('sitekey_clean', sitekey_clean)

    solve_captcha(url, sitekey_clean)

    vin_pdf = get_pdf(vin)


if __name__ == '__main__':
    main()

