import requests
from bs4 import BeautifulSoup


base_url = 'https://www.thewhiskyexchange.com'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
k = requests.get(f'{base_url}/c/35/japanese-whisky', headers=headers).text
soup = BeautifulSoup(k, 'html.parser')
product_list = soup.find_all('li', {'class': 'product-grid__item'})
product_links = []
for product in product_list:
    product_links.append(base_url + product.find('a', {'class': 'product-card'}).get('href'))

data = []

for link in product_links:
    f = requests.get(link, headers=headers).text
    hun = BeautifulSoup(f, 'html.parser')

    try:
        price = hun.find('p', {'class': 'product-action__price'}).text.replace('\n', '')
    except Exception:
        price = None
    try:
        about=hun.find('div', {'class': 'product-main__description'}).text.replace('\n', '')
    except Exception:
        about = None
    try:
        rating = hun.find('div', {'class': 'review-overview'}).text.replace('\n', '')
    except Exception:
        rating = None
    try:
        name = hun.find('h1', {'class': 'product-main__name'}).text.replace('\n', '')
    except Exception:
        name = None
    whisky = {'name': name, 'price': price, 'rating': rating, 'about': about}

    data.append(whisky)
