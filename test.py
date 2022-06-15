from anticaptchaofficial.recaptchav2proxyless import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

url = "https://bimmer.work"
driver = webdriver.Chrome(executable_path='/home/yn/Documents/chromedriver')
page = driver.get(url)

sitekey = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/form/div[3]/div').get_attribute('outerHTML')
sitekey_clean = sitekey.split('"><div style="width:')[0].split('data-sitekey="')[-1]
print('sitekey_clean', sitekey_clean)

solver = recaptchaV2Proxyless()
solver.set_verbose(1)
solver.set_key('7a0556a0ad5a2051060b0c45cd0d0740')
solver.set_website_url(url)
solver.set_website_key(sitekey_clean)

g_response = solver.solve_and_return_solution()
if g_response != 0:
    print('g-response: ' + g_response)
else:
    print('task finished with error ' + solver.error_code)

driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "{}";'.format(g_response))
driver.execute_script("onSuccess('{}')".format(g_response))
time.sleep(1)

