import requests
import bs4

response = requests.get('https://sibdroid.ru/catalog/smartfony_samsung/')
print(response.text)

bs = bs4.BeautifulSoup(response.text, 'html.parser')
phones = bs.find_all('div', class_ = 'c20-body')
for phone in phones:
    name = phone.find('span', itemprop='name').strip()
    price = phone.find('span', itemprop='offers').strip()
    rai = phone.find('b').strip
    print(f'{name.text} - {price.text} - {rai.text}')