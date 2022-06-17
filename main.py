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

    g_response = solve_captcha(url, sitekey_clean)

def change_pdf():
    pass

def main():
    url = "https://bimmer.work"
    vin = get_vin()

    vin_pdf = get_pdf(vin)

if __name__ == '__main__':
    main()

