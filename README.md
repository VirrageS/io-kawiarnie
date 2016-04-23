# IO-Kawiarnie

[![Build Status](https://travis-ci.org/VirrageS/io-kawiarnie.svg?branch=master)](https://travis-ci.org/VirrageS/io-kawiarnie)
[![Code Health](https://landscape.io/github/VirrageS/io-kawiarnie/master/landscape.svg?style=flat)](https://landscape.io/github/VirrageS/io-kawiarnie/master)

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

Potem znowu albo tworzymy nowego brancha `git checkout -b ...` albo po prostu
rozwijamy poprzedniego `git checkout ...` (bez opcji `-b`). Aby łatwo powrócić
starym branchem do poziomu mastera wystarczy:

    $ git checkout [nazwa_brancha]
    $ git rebase origin/master
    $ git push

Po tych operacjach powinniśmy być na takim samym commicie co master

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

    (venv)$ coverage run --source="." --omit="*migrations*" manage.py test
    (venv)$ coverage report
    (venv)$ coverage html
    (venv)$ cd htmlcov; open index.html; cd ..;


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
