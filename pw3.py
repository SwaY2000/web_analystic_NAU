"""На основі запрпонованого додатку: https://classroom.google.com/c/NTg3ODgxNjcwMDU5/m/NTk0MTU4OTk5NTEz/details,
подувати воасний проект з урахуванням лічильника відвідувань сторінки"""
import cherrypy
import os
import numpy as np
from scipy.optimize import curve_fit
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
import sqlite3 as sq
import time

global text
global l
global l1
global two
global date
global one
global counter

counter=0

try:
    os.makedir(r'C:\parser_whisky_shop')
except:
    pass


a2=sq.connect(r'C:\parser_whisky_shop\counter.db')
x=a2.cursor()
try:
    x.execute('''CREATE TABLE counter(
    Id INTEGER, time TEXT );''')
    a2.commit()
except:
    pass


class StringGenerator():
    @cherrypy.expose
    def index(self):
        global text
        global counter
        global l
        global l1
        global two
        global date
        global one
        r = r'C:\parser_whisky_shop\data.xls'
        import pandas as pd
        s=pd.read_excel(r)
        two=str(list(s['name2']))
        l=str(sum(s['name'])/len(s))[:-12]
        l1=str(s['name'].std())[:-12]
        one=str(list(s['name']))
        date=list(s['date'])
        date=[i.__str__() for i in date]

        a2=sq.connect(r'C:\parser_whisky_shop\counter.db')
        x=a2.cursor()
        counter = int(x.execute("select * from counter").fetchall()[-1][0])+1
        named_tuple = time.localtime()
        x.execute("insert into counter values({0},'{1}')".format(counter, time.strftime("%m-%d-%Y, %H:%M:%S", named_tuple)))
        a2.commit()

        a2=sq.connect(r'C:\parser_whisky_shop\counter.db')
        x=a2.cursor()
        f=x.execute('''select * from counter;''').fetchall()
        count=f[-1][0]
        count1=f[-1][1]



        text=open(r'C:\parser_whisky_shop\1.html', 'r', encoding ='utf-8').read()
        return '''<!doctype html>
<html lang="en">
    <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

          <body>
<nav class="navbar navbar-dark bg-dark">

<nav class="navbar navbar-light bg-light">
<!--  <div class="container-fluid">

  </div> -->
</nav>

<head><h1><p style="color:#FF0000">Додаток для парсингу</p></h1></head>


<div class="btn-group">
  <button type="button" class="btn btn-danger dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
    Отримати результати
  </button>
  <ul class="dropdown-menu">

    <li><a class="dropdown-item" href="#">

            <form method="get" action="down">
              <button type="submit">Скачать в exсel</button>
            </form></a></li>

  </ul>
</div>
</nav>

<!-- Button trigger modal -->
<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
  Launch demo modal
</button>

<!-- Modal -->
<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="exampleModalLabel">Modal title</h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <p>Кількість відвідувань сторінки - '''+str(count)+''' осіб</p>
 <p>Дата останнього звернення - '''+str(count1)+'''</p><br>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>






<div class="accordion accordion-flush" id="accordionFlushExample">
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingOne">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
        Форма для посилань на каталоги товарів
      </button>
    </h2>
    <div id="flush-collapseOne" class="accordion-collapse collapse" aria-labelledby="flush-headingOne" data-bs-parent="#accordionFlushExample">
      <div class="accordion-body">

<form method="get" action="parsing">
<input type=" " class="form-control" id="floatingInput" placeholder="" name="a">
<button type="submit">Розпочати парсинг</button>
</form>


      </div>
    </div>
  </div>




  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingTwo">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseTwo" aria-expanded="false" aria-controls="flush-collapseTwo">
        Таблиця з результатами
      </button>
    </h2>
    <div id="flush-collapseTwo" class="accordion-collapse collapse" aria-labelledby="flush-headingTwo" data-bs-parent="#accordionFlushExample">
      <div class="accordion-body">
       ''' + text + '''
       </div>
    </div>
  </div>




  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingFive">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseThree" aria-expanded="false" aria-controls="flush-collapseThree">
        Пошук ключових слів
      </button>
    </h2>
    <div id="flush-collapseThree" class="accordion-collapse collapse" aria-labelledby="flush-headingThree" data-bs-parent="#accordionFlushExample">
      <div class="accordion-body">

  <form class="d-flex" method="get" action="parsing2">
      <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" name="val">
      <button class="btn btn-outline-success" type="submit">Search</button>
    </form>

      </div>
    </div>
  </div>


   <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingTwo1">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseTwo1" aria-expanded="false" aria-controls="flush-collapseTwo1">
        Таблиця з результатами
      </button>
    </h2>
    <div id="flush-collapseTwo1" class="accordion-collapse collapse" aria-labelledby="flush-headingTwo1" data-bs-parent="#accordionFlushExample">
      <div class="accordion-body">
       <h3>Завантажити excel</h3>

<form method="post" action="upload" enctype="multipart/form-data">
    <input type="file" name="ufile" />
    <input type="submit" />
</form>
<div id='myDiv'><!-- Plotly chart will be drawn inside this DIV --></div>
<br>
<p>Середнє значення: ''' + l + '''<br>
 Відхилення: ''' + l1 + '''
       </div>
    </div>
  </div>



 <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingTwo3">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseTwo3" aria-expanded="false" aria-controls="flush-collapseTwo1">
        Робота з базами даних
      </button>
    </h2>
    <div id="flush-collapseTwo3" class="accordion-collapse collapse" aria-labelledby="flush-headingTwo3" data-bs-parent="#accordionFlushExample">
      <div class="accordion-body">


<form method="get" action="generate3">
  <div class="row">
    <div class="col">
     <h3>Таблиця книги</h3>
       <input type="text" class="form-control" name="a" placeholder="id">
       <input type="text" class="form-control" name="b" placeholder="title">
       <input type="text" class="form-control" name="c" placeholder="count_page">
       <input type="text" class="form-control" name="d" placeholder="price">
    </div>
    <div class="col">
     <h3>Таблиця автори</h3>
       <input type="text" class="form-control" name="f" placeholder="id">
        <input type="text" class="form-control" name="g" placeholder="name">
         <input type="text" class="form-control" name="h" placeholder="age">

    </div>
	    <div class="col">
     <h3>Звязки між таблицями</h3>
       <input type="text" class="form-control" name="auth_id" placeholder="auth_id">
        <input type="text" class="form-control" name="books_id" placeholder="books_id">
        <button type="submit">Пошук</k>
    </div>


  </div>
</form>

       </div>
    </div>
  </div>



</div>


    <!-- Optional JavaScript; choose one of the two! -->

    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>

    <!-- Option 2: Separate Popper and Bootstrap JS -->
    <!--
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js" integrity="sha384-7+zCNj/IqJ95wo16oMtfsKbZ9ccEh31eOz1HGyDuCQ6wgnyJNSYdrPa03rtR1zdB" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js" integrity="sha384-QJHtvGhmr9XOIpI6YVutG+2QOK9T+ZnN4kzFN1RtK3zEFEIsxhlmWl5/YESvpZ13" crossorigin="anonymous"></script>
    -->
<script>
var trace1 = {mode: "lines+markers",
  x:'''+ str(date) +''',
  y: '''+ str(one) +''',
  name: 'Вартість товару',

};

var trace2 = {mode: "lines+markers",
  x:'''+ str(date) +''',
  y: '''+ str(two) +''',
  name: 'Вартість товару',

};



var layout = {
      margin: {t:0,r:0,b:0,l:20},
      xaxis: {
        automargin: true,
        tickangle: 90,
        title: {
          text: "Дата-Времмя",
          standoff: 20
        }},
      yaxis: {
        automargin: true,
        tickangle: 90,
        title: {
          text: "Вартість товару",
          standoff: 40
        }}}

var data = [trace1, trace2];

Plotly.newPlot('myDiv', data, layout);


</script>
</body>
</html>'''



    @cherrypy.expose
    def generate3(self, a, b, c, d, f, g, h, auth_id, books_id):
        import sqlite3 as sq
        z=sq.connect(r'C:\parser_whisky_shop\base1.db')
        x=z.cursor()
        try:
            x.execute('''
CREATE TABLE books(
    Id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    count_page INTEGER NOT NULL CHECK (count_page >0),
    price REAL CHECK (price >0)
    );
        ''')
            x.execute('''
CREATE TABLE auth(

    id INTEGER PRIMARY KEY,

    name TEXT NOT NULL,

    age INTEGER  CHECK (age >16)

    );''')
            x.execute('''
CREATE TABLE auth_book (

    auth_id INTEGER NOT NULL,

    books_id INTEGER NOT NULL,

    FOREIGN KEY (auth_id) REFERENCES auth(id)

    FOREIGN KEY (books_id) REFERENCES books(id)

    );''')
        except:
            pass


        x.execute("INSERT INTO books (id, title, count_page, price) VALUES ({0}, '{1}', '{2}', '{3}');".format(a, b, c, d))
        x.execute("INSERT INTO auth (id, name, age) VALUES ({0}, '{1}', {2});".format(f, g, h))


        try:
            x.execute("INSERT INTO auth_book (auth_id, books_id) VALUES ({0}, {1});".format(auth_id, books_id))
        except:
            pass
        z.commit()
        books=x.execute('select * from books').fetchall()
        auth=x.execute('select * from auth').fetchall()
        auth_book=x.execute('select * from auth_book').fetchall()

        return '''
		<!doctype html>
<html lang="en">
    <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

          <body>
<nav class="navbar navbar-dark bg-dark">

<nav class="navbar navbar-light bg-light">
<!--  <div class="container-fluid">

  </div> -->
</nav>

<head><h1><p style="color:#FF0000">Додаток для парсингу</p></h1></head>


<div class="btn-group">
  <button type="button" class="btn btn-danger dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
    Отримати результати
  </button>
  <ul class="dropdown-menu">

    <li><a class="dropdown-item" href="#">

            <form method="get" action="down">
              <button type="submit">Скачать в exсel</button>
            </form></a></li>
  </ul>
</div>
</nav>

<div class="accordion accordion-flush" id="accordionFlushExample">
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingOne">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
        Форма для посилань на каталоги товарів
      </button>
    </h2>
    <div id="flush-collapseOne" class="accordion-collapse collapse" aria-labelledby="flush-headingOne" data-bs-parent="#accordionFlushExample">
      <div class="accordion-body">

<form method="get" action="parsing">
<input type=" " class="form-control" id="floatingInput" placeholder="" name="a">
<button type="submit">Розпочати парсинг</button>
</form>


      </div>
    </div>
  </div>




  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingTwo">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseTwo" aria-expanded="false" aria-controls="flush-collapseTwo">
        Таблиця з результатами
      </button>
    </h2>
    <div id="flush-collapseTwo" class="accordion-collapse collapse" aria-labelledby="flush-headingTwo" data-bs-parent="#accordionFlushExample">
      <div class="accordion-body">
       ''' + text + '''
       </div>
    </div>
  </div>




  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingFive">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseThree" aria-expanded="false" aria-controls="flush-collapseThree">
        Пошук ключових слів
      </button>
    </h2>
    <div id="flush-collapseThree" class="accordion-collapse collapse" aria-labelledby="flush-headingThree" data-bs-parent="#accordionFlushExample">
      <div class="accordion-body">

  <form class="d-flex" method="get" action="parsing2">
      <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" name="val">
      <button class="btn btn-outline-success" type="submit">Search</button>
    </form>

      </div>
    </div>
  </div>


   <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingTwo1">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseTwo1" aria-expanded="false" aria-controls="flush-collapseTwo1">
        Таблиця з результатами
      </button>
    </h2>
    <div id="flush-collapseTwo1" class="accordion-collapse collapse" aria-labelledby="flush-headingTwo1" data-bs-parent="#accordionFlushExample">
      <div class="accordion-body">
       <h3>Завантажити excel</h3>

<form method="post" action="upload" enctype="multipart/form-data">
    <input type="file" name="ufile" />
    <input type="submit" />
</form>
<div id='myDiv'><!-- Plotly chart will be drawn inside this DIV --></div>
<br>
<p>Середнє значення: ''' + l + '''<br>
 Відхилення: ''' + l1 + '''
       </div>
    </div>
  </div>



 <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingTwo3">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseTwo3" aria-expanded="false" aria-controls="flush-collapseTwo1">
        Робота з базами даних
      </button>
    </h2>
    <div id="flush-collapseTwo3" class="accordion-collapse collapse" aria-labelledby="flush-headingTwo3" data-bs-parent="#accordionFlushExample">
      <div class="accordion-body">


<form method="get" action="generate3">
  <div class="row">
    <div class="col">
     <h3>Таблиця книги</h3>
       <input type="text" class="form-control" name="a" placeholder="id">
       <input type="text" class="form-control" name="b" placeholder="title">
       <input type="text" class="form-control" name="c" placeholder="count_page">
       <input type="text" class="form-control" name="d" placeholder="price">
    </div>
    <div class="col">
     <h3>Таблиця автори</h3>
       <input type="text" class="form-control" name="f" placeholder="id">
        <input type="text" class="form-control" name="g" placeholder="name">
         <input type="text" class="form-control" name="h" placeholder="age">

    </div>
	    <div class="col">
     <h3>Звязки між таблицями</h3>
       <input type="text" class="form-control" name="auth_id" placeholder="auth_id">
        <input type="text" class="form-control" name="books_id" placeholder="books_id">
        <button type="submit">Пошук</k>
    </div>


  </div>
</form>

       </div>
    </div>
  </div>

''' +str(books)+ ''' <br>
''' +str(auth)+ ''' <br>
''' +str(auth_book)+ ''' <br>


</div>


    <!-- Optional JavaScript; choose one of the two! -->

    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>

    <!-- Option 2: Separate Popper and Bootstrap JS -->
    <!--
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js" integrity="sha384-7+zCNj/IqJ95wo16oMtfsKbZ9ccEh31eOz1HGyDuCQ6wgnyJNSYdrPa03rtR1zdB" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js" integrity="sha384-QJHtvGhmr9XOIpI6YVutG+2QOK9T+ZnN4kzFN1RtK3zEFEIsxhlmWl5/YESvpZ13" crossorigin="anonymous"></script>
    -->
<script>
var trace1 = {mode: "lines+markers",
  x:'''+ str(date) +''',
  y: '''+ str(one) +''',
  name: 'Вартість товару',

};

var trace2 = {mode: "lines+markers",
  x:'''+ str(date) +''',
  y: '''+ str(two) +''',
  name: 'Вартість товару',

};



var layout = {
      margin: {t:0,r:0,b:0,l:20},
      xaxis: {
        automargin: true,
        tickangle: 90,
        title: {
          text: "Дата-Времмя",
          standoff: 20
        }},
      yaxis: {
        automargin: true,
        tickangle: 90,
        title: {
          text: "Вартість товару",
          standoff: 40
        }}}

var data = [trace1, trace2];

Plotly.newPlot('myDiv', data, layout);


</script>
</body>
</html>
		'''


    @cherrypy.expose
    def upload(self, ufile):
        r=ufile.filename  # ufile относится к класу  cherrypy._cpreqbody.Part
        import pandas as pd
        s=pd.read_excel('C:\\parser_whisky_shop\\'+r)
        two=str(list(s['name2']))
        three=str(list(s['wewwe']))
        l=str(sum(s['name'])/len(s))
        l1=str(s['name'].std())[:-12]
        one=str(list(s['name']))
        date=list(s['date'])
        four=str(list(s['sqr']))

        return '''

<!doctype html>
<html lang="en">
    <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

          <body>
<nav class="navbar navbar-dark bg-dark">

<nav class="navbar navbar-light bg-light">
<!--  <div class="container-fluid">

  </div> -->
</nav>

<head><h1><p style="color:#FF0000">Додаток для парсингу</p></h1></head>


<div class="btn-group">
  <button type="button" class="btn btn-danger dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
    Отримати результати
  </button>
  <ul class="dropdown-menu">

    <li><a class="dropdown-item" href="#">

            <form method="get" action="down">
              <button type="submit">Скачать в exсel</button>
            </form></a></li>
  </ul>
</div>
</nav>

<div class="accordion accordion-flush" id="accordionFlushExample">
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingOne">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
        Форма для посилань на каталоги товарів
      </button>
    </h2>
    <div id="flush-collapseOne" class="accordion-collapse collapse" aria-labelledby="flush-headingOne" data-bs-parent="#accordionFlushExample">
      <div class="accordion-body">

<form method="get" action="parsing">
<input type=" " class="form-control" id="floatingInput" placeholder="" name="a">
<button type="submit">Розпочати парсинг</button>
</form>


      </div>
    </div>
  </div>




  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingTwo">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseTwo" aria-expanded="false" aria-controls="flush-collapseTwo">
        Таблиця з результатами
      </button>
    </h2>
    <div id="flush-collapseTwo" class="accordion-collapse collapse" aria-labelledby="flush-headingTwo" data-bs-parent="#accordionFlushExample">
      <div class="accordion-body">
       ''' + text + '''
       </div>
    </div>
  </div>




  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingFive">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseThree" aria-expanded="false" aria-controls="flush-collapseThree">
        Пошук ключових слів
      </button>
    </h2>
    <div id="flush-collapseThree" class="accordion-collapse collapse" aria-labelledby="flush-headingThree" data-bs-parent="#accordionFlushExample">
      <div class="accordion-body">

  <form class="d-flex" method="get" action="parsing2">
      <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" name="val">
      <button class="btn btn-outline-success" type="submit">Search</button>
    </form>

      </div>
    </div>
  </div>


   <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingTwo1">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseTwo1" aria-expanded="false" aria-controls="flush-collapseTwo1">
        Таблиця з результатами
      </button>
    </h2>
    <div id="flush-collapseTwo1" class="accordion-collapse collapse" aria-labelledby="flush-headingTwo1" data-bs-parent="#accordionFlushExample">
      <div class="accordion-body">
       <h3>Завантажити excel</h3>

<form method="post" action="upload" enctype="multipart/form-data">
    <input type="file" name="ufile" />
    <input type="submit" />
</form>
<div id='myDiv'><!-- Plotly chart will be drawn inside this DIV --></div>
<br>
<p>Середнє значення: ''' + l + ''' <br>
<p>Середнє квадратичне відхилення: ''' + l1 + ''' <br>
Лінія тренду:

       </div>
    </div>
  </div>




</div>


    <!-- Optional JavaScript; choose one of the two! -->

    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>

    <!-- Option 2: Separate Popper and Bootstrap JS -->
    <!--
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js" integrity="sha384-7+zCNj/IqJ95wo16oMtfsKbZ9ccEh31eOz1HGyDuCQ6wgnyJNSYdrPa03rtR1zdB" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js" integrity="sha384-QJHtvGhmr9XOIpI6YVutG+2QOK9T+ZnN4kzFN1RtK3zEFEIsxhlmWl5/YESvpZ13" crossorigin="anonymous"></script>
    -->
<script>
var trace1 = {mode: "lines+markers",
  x:'''+ str(date) +''',
  y: '''+ str(one) +''',
  name: 'Вартість товару',

};

var trace2 = {mode: "lines+markers",
  x:'''+ str(date) +''',
  y: '''+ str(two) +''',
  name: 'Вартість товару',

};

var trace3 = {mode: "lines+markers",
  x:'''+ str(date) +''',
  y: '''+ str(three) +''',
  name: 'Вартість товару',

};

var layout = {
      margin: {t:0,r:0,b:0,l:20},
      xaxis: {
        automargin: true,
        tickangle: 90,
        title: {
          text: "Дата-Времмя",
          standoff: 20
        }},
      yaxis: {
        automargin: true,
        tickangle: 90,
        title: {
          text: "Вартість товару",
          standoff: 40
        }}}

var data = [trace1, trace2, trace3];

Plotly.newPlot('myDiv', data, layout);


</script>
</body>
</html>

'''


    @cherrypy.expose
    def down(self):

        return cherrypy.lib.static.serve_file(r'C:\parser_whisky_shop\1.xls', content_type='xls', disposition='attachment', name='1.xls')

    @cherrypy.expose
    def parsing2(self, val):
        import pandas as pd
        import sqlite3 as sq
        base=sq.connect(r'C:\parser_whisky_shop\base.db')
        b=pd.read_html(r'C:\parser_whisky_shop\1.html')
        base.execute('drop table if exists www')
        b[0].to_sql('www', con = base)
        res = base.execute("SELECT * FROM www WHERE name LIKE '%{}%'".format(val)).fetchone()
        try:
            res0=str(res[-1])
            res1=str(res[-2])
            res2=str(res[-3])
        except:
            res0='за вашим запитом нічого не значдено'
            res1='за вашим запитом нічого не значдено'
            res2='за вашим запитом нічого не значдено'
        text=open(r'C:\parser_whisky_shop\1.html', 'r').read()
        return '''
    <!doctype html>
<html lang="en">
    <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

          <body>
<nav class="navbar navbar-dark bg-dark">

<nav class="navbar navbar-light bg-light">
<!--  <div class="container-fluid">

  </div> -->
</nav>

<head><h1><p style="color:#FF0000">Додаток для парсингу</p></h1></head>


<div class="btn-group">
  <button type="button" class="btn btn-danger dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
    Отримати результати
  </button>
  <ul class="dropdown-menu">

    <li><a class="dropdown-item" href="#">

            <form method="get" action="down">
              <button type="submit">Скачать в exсel</button>
            </form></a></li>
  </ul>
</div>
</nav>

<div class="accordion accordion-flush" id="accordionFlushExample">
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingOne">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
        Форма для посилань на каталоги товарів
      </button>
    </h2>
    <div id="flush-collapseOne" class="accordion-collapse collapse" aria-labelledby="flush-headingOne" data-bs-parent="#accordionFlushExample">
      <div class="accordion-body">

<form method="get" action="parsing">
<input type=" " class="form-control" id="floatingInput" placeholder="" name="a">
<button type="submit">Розпочати парсинг</button>
</form>


      </div>
    </div>
  </div>
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingTwo">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseTwo" aria-expanded="false" aria-controls="flush-collapseTwo">
        Таблиця з результатами
      </button>
    </h2>
    <div id="flush-collapseTwo" class="accordion-collapse collapse" aria-labelledby="flush-headingTwo" data-bs-parent="#accordionFlushExample">
      <div class="accordion-body">
      ''' + text + '''
       </div>
    </div>
  </div>
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingThree">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseThree" aria-expanded="false" aria-controls="flush-collapseThree">
        Пошук ключових слів
      </button>
    </h2>
    <div id="flush-collapseThree" class="accordion-collapse collapse" aria-labelledby="flush-headingThree" data-bs-parent="#accordionFlushExample">
      <div class="accordion-body">

  <form class="d-flex" method="get" action="parsing2">
      <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" name="val">
      <button class="btn btn-outline-success" type="submit">Search</button>
    </form>

    <p> <h5> Характеристика товару: -''' + res0 + ''' </h5></p> <br>
    <p> <h5> Рейтинг товару: -''' + res1 + ''' </h5></p> <br>
    <p> <h5> Ціна товару: -''' + res2 + ''' </h5></p>

      </div>
    </div>
  </div>
</div>


    <!-- Optional JavaScript; choose one of the two! -->

    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>

    <!-- Option 2: Separate Popper and Bootstrap JS -->
    <!--
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js" integrity="sha384-7+zCNj/IqJ95wo16oMtfsKbZ9ccEh31eOz1HGyDuCQ6wgnyJNSYdrPa03rtR1zdB" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js" integrity="sha384-QJHtvGhmr9XOIpI6YVutG+2QOK9T+ZnN4kzFN1RtK3zEFEIsxhlmWl5/YESvpZ13" crossorigin="anonymous"></script>
    -->

</body>
</html>'''



    @cherrypy.expose
    def parsing(self, a):
        try:
            os.mkdir(r'C:\parser_whisky_shop')
        except:
            pass
        os.chdir(r'C:\parser_whisky_shop')
        baseurl = "https://www.thewhiskyexchange.com"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        k = requests.get(a).text
        soup=BeautifulSoup(k,'html.parser')
        productlist = soup.find_all("li",{"class":"product-grid__item"})
        productlinks = []
        for product in productlist:
            productlinks.append(baseurl + product.find("a",{"class":"product-card"}).get('href'))


        data=[]

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
            df = pd.DataFrame(data)
            df.to_html('1.html')
            df.to_excel('1.xls')
            res=''
            text=open(r'C:\parser_whisky_shop\1.html', 'r').read()
           #re.sub('<table border="1" class="dataframe">', '<table class="table table-dark table-hover">', text )



        return '''<!doctype html>
<html lang="en">
    <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

          <body>
<nav class="navbar navbar-dark bg-dark">

<nav class="navbar navbar-light bg-light">
<!--  <div class="container-fluid">

  </div> -->
</nav>

<head><h1><p style="color:#FF0000">Додаток для парсингу</p></h1></head>


<div class="btn-group">
  <button type="button" class="btn btn-danger dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
    Отримати результати
  </button>
  <ul class="dropdown-menu">

    <li><a class="dropdown-item" href="#">

            <form method="get" action="down">
              <button type="submit">Скачать в exсel</button>
            </form></a></li>
  </ul>
</div>
</nav>

<div class="accordion accordion-flush" id="accordionFlushExample">
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingOne">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
        Форма для посилань на каталоги товарів
      </button>
    </h2>
    <div id="flush-collapseOne" class="accordion-collapse collapse" aria-labelledby="flush-headingOne" data-bs-parent="#accordionFlushExample">
      <div class="accordion-body">

<form method="get" action="parsing">
<input type=" " class="form-control" id="floatingInput" placeholder="" name="a">
<button type="submit">Розпочати парсинг</button>
</form>


      </div>
    </div>
  </div>
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingTwo">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseTwo" aria-expanded="false" aria-controls="flush-collapseTwo">
        Таблиця з результатами
      </button>
    </h2>
    <div id="flush-collapseTwo" class="accordion-collapse collapse" aria-labelledby="flush-headingTwo" data-bs-parent="#accordionFlushExample">
      <div class="accordion-body">
''' + text + '''

</div>
    </div>
  </div>
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingThree">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseThree" aria-expanded="false" aria-controls="flush-collapseThree">
        Пошук ключових слів
      </button>
    </h2>
    <div id="flush-collapseThree" class="accordion-collapse collapse" aria-labelledby="flush-headingThree" data-bs-parent="#accordionFlushExample">
      <div class="accordion-body">

  <form class="d-flex" method="get" action="parsing2">
      <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" name="val">
      <button class="btn btn-outline-success" type="submit">Search</button>
    </form>

    <p>''' + res + ''' </p>

      </div>
    </div>
  </div>
</div>


    <!-- Optional JavaScript; choose one of the two! -->

    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>

    <!-- Option 2: Separate Popper and Bootstrap JS -->
    <!--
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js" integrity="sha384-7+zCNj/IqJ95wo16oMtfsKbZ9ccEh31eOz1HGyDuCQ6wgnyJNSYdrPa03rtR1zdB" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js" integrity="sha384-QJHtvGhmr9XOIpI6YVutG+2QOK9T+ZnN4kzFN1RtK3zEFEIsxhlmWl5/YESvpZ13" crossorigin="anonymous"></script>
    -->  <table class="table table-dark">
  <thead>
    ...
  </thead>
  <tbody>


</body>
</html>'''


cherrypy.quickstart(StringGenerator())