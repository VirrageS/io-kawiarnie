# IO-Kawiarnie

[![Build Status](https://travis-ci.org/VirrageS/io-kawiarnie.svg?branch=master)](https://travis-ci.org/VirrageS/io-kawiarnie)
[![Code Health](https://landscape.io/github/VirrageS/io-kawiarnie/master/landscape.svg?style=flat)](https://landscape.io/github/VirrageS/io-kawiarnie/master)
[![Coverage Status](https://coveralls.io/repos/github/VirrageS/io-kawiarnie/badge.svg?branch=master)](https://coveralls.io/github/VirrageS/io-kawiarnie?branch=master)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/b312147765aa43fba60a38df7c012019/badge.svg)](https://www.quantifiedcode.com/app/project/b312147765aa43fba60a38df7c012019)

## Workflow

Każdą nową funkcjonalność dodajemy poprzez stworzenie nowego brancha,
napisanie funkcjonalności, napisanie do niej testów i wmergowania
funkcjonalności do mastera.

    $ git checkout -b [nazwa_brancha]
    $ ... commits ...

Odpalamy przeglądarkę, wchodzimy na githubie na naszego brancha i
klikamy `Pull request`. Następnie czekamy na łapki w góre i jeżeli
wszystko jest zatwierdzone mergujemy pull requesta. Później usuwamy
nieużywane branche:

    $ git checkout master
    $ git pull
    $ git push origin --delete [nazwa_brancha]
    $ git fetch --all --prune
    $ git branch --merged master | grep -v 'master$' | xargs git branch -d

Potem znowu tworzymy nowego brancha `git checkout -b ...` i zaczynamy
cykl od nowa.

## Setup

Jeżeli nie macie `virtualenv` to ściągnijcie:

    $ pip install virtualenv

Teraz tworzymy środowisko

    $ git clone git@github.com:VirrageS/io-kawiarnie.git
    $ cd io-kawiarnie
    $ virtualenv -p python3 venv
    $ . venv/bin/activate
    (venv)$ pip install --upgrade pip
    (venv)$ pip install -r requirements.txt

Teraz jesteśmy gotowi, aby odpalić serwer:

    (venv)$ cd caffe
    (venv)$ python manage.py migrate
    (venv)$ python manage.py runserver

## Testing

Do testowania używamy `coverage`. Aby użyć tego narzędzia wystarczy wpisać.

    (venv)$ coverage run --source="caffe" --omit="*migrations*, *venv*, *env*" caffe/manage.py test caffe
    (venv)$ coverage report
    (venv)$ coverage html
    (venv)$ open htmlcov/index.html


1. W pierwszej linijce, na końcu możemy wyspecifkować jaką aplikację teraz
testujemy np. `reports` lub `employees`.
2. W drugiej generujemy raport na podstawie testów jakie przeszły. Możemy także
dodać opcję `-m`, która dokładnie pokaże nam linijki, które nigdy się nie
wykonały w testach (!).
3. W trzeciej linijce generujemy html'owy raport, w którym dokładnie możemy
sprawdzić, jakie części kodu się wykonały, a które nie. Super przydatne i ładne.
4. Czwarta linijka to proste makro, które odpala nam html'owy raport w
przeglądarce.

## Code Quality

Jednym z narzędzi, których będziemy używać jest `pep8`. Używamy go
w katologu, który chcemy sprawdzić jakość naszego kodu. Przechodzi
rekursywnie po folderach, więc jest spoko.

    (venv)$ pep8 .

Drugim z nich (narzędzi) jest `pylint`. Bardzo fajne narzędzie, bo przyznaje
punkty dla naszego kodu :) Musimy mieć zainstalowny `pylint-django` żeby był
mądry i nie wywalał błędów, które wynikają ze struktury Django i jego aplikacji.

    (venv)$ pylint --load-plugins=pylint_django reports

Ostatni parametr `reports` mówi dla `pylint`, którą aplikację chcemy
przetestować. Czasami błędy są głupie, no i nie da ich poprawić, wtedy po prostu
zostawiamy - trudno...

## Rules

1. Komentarze w kodzie piszemy po angielsku
2. Nazwy commitów piszemy po angielsku
3. Nazwy zmiennych, funkcji piszemy po angielsku
4. Staramy się niszczyć rzeczy we własnych branchach, a nie masterze
5. Wszystkie możliwe funkcjonalności powinny mieć swoje testy - najlepiej przed
wrzuceniem do mastera.
6. Próbujmy pisać ładny kod, dlatego używamy `pep8` i `pylint`
