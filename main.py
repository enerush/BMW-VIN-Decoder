from anticaptchaofficial.recaptchav2proxyless import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import telebot
import requests
import time
import os

from dotenv import load_dotenv
load_dotenv()


def check_vin(vin: str) -> bool:
    """Checks VIN for correctness"""

    vin = vin.upper()
    if len(vin) == 17 and vin[0:3] in ('WBA', 'WBY', 'WBS', '5YM', '5UX'):
        print('VIN is correct.')
        return True
    return False


def save_pdf(url_pdf: str, vin: str) -> None:
    """Saves the PDF file in the project directory"""

    pdf_data = requests.get(url_pdf)
    pdf_name = vin + '.pdf'
    print(f'Saving: {vin}')

    with open('./Storage/' + pdf_name, 'wb') as file:
        file.write(pdf_data.content)


def solve_recaptcha(url: str, sitekey: str) -> str:
    """Solves the reCaptcha"""

    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(os.getenv('ANTICAPTCHA_KEY'))
    solver.set_website_url(url)
    solver.set_website_key(sitekey)

    g_response = solver.solve_and_return_solution()
    if g_response != 0:
        print('g_response: ', g_response)
        return g_response
    else:
        print('task finished with error ' + solver.error_code)


def get_url_pdf(vin: str):
    """Parses the third-party resource
    and returns a URL to the PDF decoding
    of the requested VIN"""

    url = os.getenv('URL')

    chromeOptions = Options()
    chromeOptions.headless = True
    driver = webdriver.Chrome(executable_path='./chromedriver', options=chromeOptions)
    driver.get(url)

    vin_form = driver.find_element(By.NAME, "vin")
    vin_form.send_keys(vin)

    sitekey = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/form/div[3]/div').get_attribute(
        'outerHTML')
    sitekey_clean = sitekey.split('"><div style="width:')[0].split('data-sitekey="')[-1]
    print('Sitekey_clean: ', sitekey_clean)

    g_response = solve_recaptcha(url, sitekey_clean)

    driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="";')
    driver.execute_script("""document.getElementById("g-recaptcha-response").innerHTML = arguments[0]""", g_response)
    driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="none";')
    vin_form.send_keys(Keys.ENTER)
    time.sleep(16)

    # Checks if the third-party service has processed our request correctly
    if driver.current_url == 'https://bimmer.work/query.php':
        return False

    url_pdf = driver.current_url[:-1] + '.pdf'
    print('URL to PDF: ', url_pdf)
    driver.quit()
    return url_pdf


def telegram_bot(token: str) -> None:
    """Initiating the Telegram bot"""
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        """Sends a welcome message"""
        bot.send_message(message.chat.id, 'My name is Hans, I am from Munich. I know how to decode the equipment of\
                                            your BMW! Just send me the VIN number:')

    @bot.message_handler(content_types=["text"])
    def handle_text(message):
        """Sends a PDF file with the equipment list of the requested VIN code"""

        vin = message.text
        print(f'Processing: {vin}')
        bot.send_message(message.chat.id, "Processing your request, it takes a few minutes...")

        if check_vin(vin):
            if os.path.exists('./Storage/' + vin + '.pdf'):
                bot.send_document(message.chat.id, document=open('./Storage/' + vin + '.pdf', 'rb'))
                print('This VIN was already processed!')
                print('The process is complete!')

            else:
                url_pdf = get_url_pdf(vin)
                if url_pdf:
                    save_pdf(url_pdf, vin)
                    bot.send_document(message.chat.id, document=open('./Storage/' + vin + '.pdf', 'rb'))
                    print('The process is complete!')
                else:
                    bot.send_message(message.chat.id, 'Incorrect VIN number or something went wrong. Try again!')

        else:
            bot.send_message(message.chat.id, 'Incorrect VIN number or something went wrong. Try again!')

    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as _ex:
            print(_ex)
            time.sleep(15)


def main() -> None:
    telegram_bot(os.getenv('BOT_TOKEN'))


if __name__ == '__main__':
    main()






