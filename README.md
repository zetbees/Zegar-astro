# Zegar-astro

!!!
PROGRAM DO URUCHOMIENIA TO: zegar_hapcan.py 
!!!

Program służący do czasowego włączania i wyłączania poszczególnych modułów przekaźników systemu Hapcan

ver. alfa 0.1

Potrzebny uzupełniony plik hapcan.ini
Zawarte są w nim podstawowe informacje połaczenia z interfejsem ethernet
oraz współrzędne geograficzne miejsca użytkowania programu - na tej podstawie program wylicza wschód i zachód słońca

Potrzebny plik komendy_zegara.csv
plik opracowany w excellu lub podobnym, WAŻNE separatorem musi być średnik - ;
struktura pliku:
typ czasu - H godzina podana w rubryce [czas] w formacie HH:MM
          - W czas w minutach przed lub po wschodzie słońca podany w rubryce [czas] w formacie MM (wartość ujemna przed wschodem)
          - Z czas w minutach przed lub po zachodzie słońca podany w rubryce [czas] w formacie MM (wartość ujemna przed wschodem)

dni tygodnia - informacja w jakie dni tygodnia ma działać dana komenda 
format: tylko duże litery
- P - poniedziałek
- W - wtorek
- R - środa
- C - czwartek
- T - piątek
- S - sobota
- N - niedziela
Jeśli dana litera jest wpisana to komenda wykonywana jest w ten dzień tygodnia, jeśli nie to komenda jest pomijana.
np. PWRCTSN - komenda będzie działać w każdym dniu tygodnia
    RT - tylko w środy i piątki

pole komenda - zawsze wpisane "P" - jak przekaźnik - na razie działa tylko z przekaźnikami

moduł, grupa, nr przekaźnika - liczby całkowite oznaczające pozycję przekaźnika w systemi Hapcan

ON/OFF - włącz/wwyłącz

pole czas i warunki - do przyszłych wersji - na razie nie wykorzystywane
