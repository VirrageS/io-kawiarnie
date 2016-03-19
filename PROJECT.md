## Opis

Aplikacja webowa, która zastąpi papierowe raporty tworzone każdego dnia w kawiarni. Ułatwi wprowadzanie i przeglądanie danych.

## Grupa użytkowników

Założyciele i pracownicy kawiarni

## Funkcjonalności

**Key features**:
* Zarządzanie użytkownikami poprzez konto admina i możliwość sprawdzenia
między innymi: ilości przepracowanych godzin, historii raportów
* Możliwość dodawania raportów porannych, w ciągu dnia i na zakończenie
* Możliwość tworzenia szablonów raportów, tak aby zaoszczędzić czas
na przepisywanie tego samego
* Możliwość dodawania nowych rzeczy do raportu i tworzenie kategorii, tak
aby była większa czytelność i łatwiejsza nawigacja
* Możliwość podglądu przez admina wszystkich raportów i sprawdzenia wszystkich
zawartych w nim informacji

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

## Narzędzia

* GitHub (repository): [link](https://github.com/VirrageS/io-kawiarnie)
* Waffle (issue tracker): [link](https://waffle.io/VirrageS/io-kawiarnie)

## Harmonogram

### Iteracja 1

**Zakres**: Stworzenie admina i możliwość dodawania nowych użytkowników.
Możliwość dodawania nowych produktów, kategorii, szablonów i ich modyfikacji.
Dokument specyfikacji wymagań.

**Deadline**: 26/04

### Iteracja 2

**Zakres**: Szablon raportu porannego, w ciągu dnia, na zakończenie i
możliwość zapisywania raportów do bazy danych.
Architektura (widok logiki, widok fizyczny wdrażania).

**Deadline**: 31/05

### Iteracja 3

**Zakres**: Dostęp do wszystkich raportów przez admina; Możliwość dostępu
do informacji o każdym pracowniku: godziny przepracowane, historia raportów,
różnice z kasy.

**Deadline**: 21/06

### Iteracja 4 (jeżeli się uda)

**Zakres**: Grafik + kalendarz; Dostawy - monitorowanie produktów (ich ilości).

**Deadline**: TBA


### Iteracja 5 (jeżeli się uda)

**Zakres**: Zrobienie formularza w trybie on-going tj. byłby zapisywany co stały
okres czasu np. 10 sekund. To pozwoliłoby na nieutracenie danych podczas jego
tworzenia i zabezpieczyłoby (w pewnym sensie) przed problemami z internetem.

**Deadline**: TBA
