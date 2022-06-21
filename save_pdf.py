import requests

def save_pdf(link_pdf):
    pdf_data = requests.get(link_pdf)
    filename = vin
    print(f'Saving {filename}')
    with open('/home/yn/Downloads/' + filename, 'wb') as file:
        file.write(pdf_data.content)
