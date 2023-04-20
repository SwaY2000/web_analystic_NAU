import cherrypy
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import pandas as pd
import re

class StringGenerator(object):
    @cherrypy.expose
    def index(self, link2='1', link3='2', link4='3', link1='https://www.thewhiskyexchange.com/b/305/cardrona-rest-of-the-world-whisky'):
        data=[]
        for i1 in [link1, link2, link3, link4]:

            for i in [1,2,3]:
                baseurl = "https://www.thewhiskyexchange.com"
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
                try:
                    k = requests.get(i1+'?pg={0}'.format(i), headers=headers).text
                except:
                    pass
                soup=BeautifulSoup(k,'html.parser')
                productlinks = []

                productlist = soup.find_all("li",{"class":"product-grid__item"})
                for product in productlist:
                    productlinks.append(baseurl + product.find("a",{"class":"product-card"}).get('href'))

                for link in productlinks:
                    f = requests.get(link,headers=headers).text
                    hun=BeautifulSoup(f,'html.parser')

                    try:
                        price=hun.find("p",{"class":"product-action__price"}).text.replace('\n',"")
                    except:
                        price = None

                    try:
                        about=hun.find("div",{"class":"product-main__description"}).text.replace('\n',"")
                    except:
                        about=None

                    try:
                        rating = hun.find("div",{"class":"review-overview"}).text.replace('\n',"")
                    except:
                        rating=None

                    try:
                        name=hun.find("h1",{"class":"product-main__name"}).text.replace('\n',"")
                    except:
                        name=None

                    whisky = {"name":name,"price":price,"rating":rating,"about":about}

                    data.append(whisky)
        x=[]
        y=[]
        b=pd.DataFrame(data)
        for i,q in zip(b['price'], b['name']):
            try:
                y.append(float(re.sub('£', '', i)))
            except:
                pass
            x.append(q)
        f=pd.DataFrame(data)
        f.to_excel(r'C:\Users\1\Desktop\test_27_09_22\qqqqqqqqqqqqqqqqqqqqqq\test.xls')

        return '''
    <!DOCTYPE html>
<html lang="ua">

<head>
  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport">
  <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
  <title>Результати парсінгу</title>
      <p>
    <form method="get" action="index">
      <input type="text" value="" name="link1" /><br>
      <input type="text" value="" name="link2" /><br>
      <input type="text" value="" name="link3" /><br>
      <input type="text" value="" name="link4" /><br>
      <button type="submit">Вставить посилання</button>
    </form>
    </p><p>
    <p>Значення аргументів:</p> '''+ link2+'''<br>'''+ link3+'''<br>'''+ link4+'''<br>
  <div id='myDiv'>



<script>

var data = [
  {
    x: '''+ str(x) +''',
    y: '''+ str(y) +''',
    type: 'bar'
  }
];
Plotly.newPlot('myDiv', data);


</script>
    '''

cherrypy.quickstart(StringGenerator())

##https://www.thewhiskyexchange.com/gift-ideas
##https://www.thewhiskyexchange.com/c/730/rose-sparkling-wine
##https://www.thewhiskyexchange.com/c/611/prosecco
