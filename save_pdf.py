import requests
pdf_data = requests.get('https://bimmer.work/vin/c39d6056c031e8833672b2989f184fe67.pdf')
filename = 'vin_pdf'
print(f'Saving {filename}')
with open('/home/yn/Downloads/' + filename,'wb') as file:
    file.write(pdf_data.content)