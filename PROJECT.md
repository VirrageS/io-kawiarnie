## Opis

Aplikacja webowa, która zastąpi papierowe raporty tworzone każdego dnia w kawiarni. Ułatwi wprowadzanie i przeglądanie danych.

## Grupa użytkowników

Założyciele i pracownicy kawiarni.

## Funkcjonalności

**Key features**:
* Możliwość dodawania raportów porannych, w ciągu dnia i na
zakończenie - (raporty dotyczą stanu produktów i pieniędzy w kasie)
* Zarządzanie użytkownikami poprzez konto admina i możliwość sprawdzenia
między innymi: ilości przepracowanych godzin, historii raportów
* Możliwość podglądu przez admina wszystkich raportów i sprawdzenia wszystkich
zawartych w nim informacji
* Możliwość dodawania nowych rzeczy do raportu i tworzenie kategorii, tak
aby była większa czytelność i łatwiejsza nawigacja
* Możliwość tworzenia szablonów raportów, tak aby zaoszczędzić czas
na przepisywanie tego samego

**Extra**:
* Możliwość zmiany grafiku przez poszczególnych pracowników (zmiany będą musiały
zostać zatwierdzone przez kogoś).
* Możliwość podglądu całego kalendarza, tak aby sprawdzić kto i kiedy pracuje
lub będzie pracował
* Możliwość monitorowania poszczególnych produktów tj. ich ilości i coś
na zasadzie 'alertów', które by mówiły, że coś trzeba już zamówić

## Technologie

* Django (Python)
* JavaScript
* Docker
* Travis-CI

## Narzędzia

* GitHub (repository): [link](https://github.com/VirrageS/io-kawiarnie)
* Waffle (issue tracker): [link](https://waffle.io/VirrageS/io-kawiarnie)

## Harmonogram

### Iteracja 1

**Zakres**: Możliwość tworzenia nowych raportów.  Możliwość dodawania nowych produktów, kategorii do raportów i możliwość edycji.

Dokument specyfikacji wymagań.

**Deadline**: 18/04

### Iteracja 2

**Zakres**: Możliwość tworzenia i edytowania szablonów raportów. Możliwość tworzenia raportu z wcześniej stworzonego szablonu (np. szablonu "porannego", "wieczornego" czy "w ciągu dnia").

**Deadline**: 03/05

### Iteracja 3

**Zakres**: Stworzenie admina i możliwość dodawania nowych użytkowników.
Architektura (widok logiki, widok fizyczny wdrażania).

**Deadline**: 16/05

### Iteracja 4

**Zakres**: Dostęp do wszystkich raportów przez admina; Możliwość dostępu
do informacji o każdym pracowniku: godziny przepracowane, historia raportów,
różnice z kasy.

**Deadline**: 03/06

### Iteracja 5

**Zakres**: Grafik + kalendarz dla pracowników (godziny pracy tj. kto, kiedy pracuje).
Dostawy - monitorowanie produktów (ich ilości).

**Deadline**: 21/06
