# Projektowanie i symulacja algorytmów

## Temat projektu i problem
Problemem, jakim się ten projekt będzie problem wyznaczania tras pojazdów - VRP (Vehicle Routing Problem).
Jest to jeden z przypadków rozszerzenia komiwojazera.

Problem wyznaczania tras pojazdów (VRP) polega na wyznaczeniu optymalnych tras dla floty pojazdów, które muszą dostarczyć towary do wielu miejsc, minimalizując całkowity koszt transportu. Celem jest zminimalizowanie odległości pokonanej przez wszystkie pojazdy, jednocześnie uwzględniając wybrane ograniczenia, takie jak:
 - pojemnosc pojazdów \
    `Każdy pojazd ma ograniczoną pojemność, co oznacza, że może zabrać tylko określoną liczbę ładunków`
 - okna czasowe \
    `Niektóre miejsca docelowe mogą wymagać dostawy w określonym przedziale czasowym`
 - maksymalny czas pracy kierowców \
    `Każdy pojazd (kierowca) może mieć ograniczony czas pracy lub dzienny limit przejechanych kilometrów`
 - liczba pojazdów \
    `Flota pojazdów może być ograniczona do określonej liczby, co wpływa na planowanie tras`
 - koszty operacyjne \
    `Różne pojazdy mogą mieć różne koszty operacyjne, takie jak paliwo, opłaty drogowe, itp.`
 - różne typy pojazdów \
    `Flota może składać się z różnych typów pojazdów, które mają różne pojemności i koszty`
 - ograniczenia drogowe \
    `Niektóre drogi mogą mieć ograniczenia dotyczące wagi lub rozmiaru pojazdów`
 - priorytety dostaw \
    `Niektóre dostawy mogą mieć wyższy priorytet i muszą być dostarczone wcześniej`


Jak widac ograniczen nałozyc mozna wiele. My bazowo zdecydowaliśmy się na nałozenie limitu liczby pojazdów.

## Dane
Do implementacji algorytmów będziemy pracowac na syntetycznie generowanych grafach nie-skierowanych.

## Algorytmy
Planowo zestawimy ze sobą trzy algorytmy, przy czym skupimy się na tym najbardziej skomplikowanym - genetycznym. Postaramy się dokonac jego fine-tuningu aby działał efektywnie i skutecznie.

### Przegląd zupełny
Mozliwy do zastosowania dla małej liczby celów. Polega na przejrzeniu wszystkich dostępnych opcji. Daje gwarancję znalezienia najlepszego rozwiązania przy bardzo duzym koszcie obliczeniowym.

### Losowy
Nie daje nam gwarancji znalezienia optymalnego rozwiązania, za to działa szybko i przyjemnie dla dowolnego rozmiaru zbioru wierzchołków.

### Genetyczny
Reprezentacja chromosomu: \
`Każdy chromosom reprezentuje możliwe przypisanie klientów do tras pojazdów (kolejność odwiedzanych miejsc).` \
Ocena fitness: \
`Funkcja oceny może obejmować całkowitą pokonaną odległość, czas dostawy, koszty paliwa, liczbę pojazdów użytych itp.`\
Krzyżowanie i mutacja: \
`Tworzenie nowych rozwiązań poprzez wymianę części tras między pojazdami lub wprowadzanie drobnych zmian w kolejności obsługi klientów.` \
Selekcja: \
`Najlepsze trasy przechodzą do kolejnych iteracji, co zbliża algorytm do optymalnych rozwiązań.`\

## Wykres Gantta