# IO-Kawiarnie

[![Build Status](https://travis-ci.org/VirrageS/io-kawiarnie.svg?branch=master)](https://travis-ci.org/VirrageS/io-kawiarnie)

## Workflow

Każdą nową funkcjonalność dodajemy poprzez stworzenie nowego brancha,
napisanie funkcjonalności, napisanie do niej testów i wmergowania
funkcjonalności do mastera.

    $ git checkout -b [nazwa_brancha]
    $ ... commits ...
    $ git checkout master
    $ git pull origin master
    $ git merge [nazwa_brancha]
    $ git push origin master

## Setup

Jeżeli nie macie `virtualenv` to ściągnijcie:

    $ pip install virtualenv

Teraz tworzymy środowisko

    $ git clone git@github.com:VirrageS/io-kawiarnie.git
    $ cd io-kawiarnie
    $ virtualenv -p python3 venv
    $ . venv/bin/activate
    (venv)$ pip install -r requirements.txt

Teraz jesteśmy gotowi, aby odpalić serwer:

    (venv)$ cd caffe
    (venv)$ python3 manage.py migrate
    (venv)$ python3 manage.py runserver


## Rules

1. Komentarze w kodzie piszemy po angielsku
2. Nazwy commitów piszemy po angielsku
3. Nazwy zmiennych, funkcji piszemy po angielsku
