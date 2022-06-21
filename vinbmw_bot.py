import telebot
from anticaptchaofficial.recaptchav2proxyless import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests


def chek_vin(vin):
    if len(vin) == 17 and (vin.startswith('WBA') or vin.startswith('WBS')):
        return True
    return False

def get_url_pdf(vin):
    url = "https://bimmer.work"
    driver = webdriver.Chrome(executable_path='/home/yn/Documents/chromedriver')
    page = driver.get(url)

    vin_form = driver.find_element(By.NAME, "vin")
    vin_form.send_keys(vin)

    sitekey = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/form/div[3]/div').get_attribute(
        'outerHTML')
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

    driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="";')
    driver.execute_script("""document.getElementById("g-recaptcha-response").innerHTML = arguments[0]""", g_response)
    driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="none";')
    vin_form.send_keys(Keys.ENTER)

    current_url = driver.current_url
    if current_url == 'https://bimmer.work/query.php':
        return False
    url_pdf = driver.current_url[:-1] + '.pdf'
    return url_pdf

def save_pdf(url_pdf, vin):
    pdf_data = requests.get(url_pdf)
    filename = vin
    print(f'Saving {filename}')
    with open('/home/yn/Downloads/' + filename, 'wb') as file:
        file.write(pdf_data.content)



bot = telebot.TeleBot('5354469343:AAGWE1InCY7xbNwOih3ySjllTSD4tF6-Uow')


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Just send me the VIN number...')


@bot.message_handler(content_types=["text"])
def handle_text(message):
    vin = message.text

    if chek_vin(vin):
        url_pdf = get_url_pdf(vin)

        if url_pdf:
            save_pdf(url_pdf, vin)
        else:
            bot.send_message(message.chat.id, 'Incorrect VIN number or something went wrong. Try again...')


        bot.send_document(message.chat.id, document=open('/home/yn/Downloads/' + vin, 'rb'))
    else:
        bot.send_message(message.chat.id, 'Incorrect VIN number or something went wrong. Try again...')


bot.polling(none_stop=True, interval=0)
