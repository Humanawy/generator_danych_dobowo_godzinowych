# Generator Danych Dobowo-Godzinowych

## Opis projektu
Projekt `Generator Danych Dobowo-Godzinowych` jest narzędziem służącym do generowania danych godzinowych na podstawie dostarczonych profili zużycia, stref czasowych i szablonów płacht godzinowych. Jego głównym celem jest przetworzenie i agregacja danych w sposób umożliwiający analizę zużycia energii dla zdefiniowanych parametrów.

## Funkcjonalności
- Wczytywanie profili zużycia i stref czasowych z plików Excel (.xlsx) oraz Parquet (.parquet).
- Dostosowanie profili zużycia do formatu danych godzinowych.
- Agregacja danych z różnych źródeł i generowanie zestawień w formacie godzinowym.
- Zapis przetworzonych danych do plików Excel z podziałem na odpowiednie arkusze.

## Instalacja
Aby uruchomić projekt, należy sklonować repozytorium lub pobrać źródła projektu, a następnie zainstalować wymagane zależności:

`pip install pandas openpyxl pyarrow`

## Użycie
1. Przygotuj pliki z profilami zużycia i strefami czasowymi w odpowiednich katalogach.
2. Uruchom skrypt `main.py`, lub `qui.pyw` (moduł z interfejsem graficznym), który poprosi o ścieżkę do pliku z danymi wejściowymi (np. ścieżka do pliku Excel z informacjami niezbędnymi do generowania danych).
3. Po przetworzeniu danych, skrypt zapisze wyniki do katalogu wyjściowego.

## Struktura projektu
- `wczytaj_profile_z_katalogu_excel` i `wczytaj_profile_z_katalogu_parquet`: Funkcje do wczytywania profili zużycia z katalogów.
- `GeneratorDanychDobowoGodzinowych`: Klasa generująca dane dobowo-godzinowe na podstawie dostarczonych danych wejściowych.
- `AgregatorGeneratorow`: Klasa agregująca wyniki z różnych generatorów i zapisująca do plików Excel.

## Opis arkuszy wynikowych
Program generuje pliki Excel składające się z czterech arkuszy: Tabela przestawna, Lista scalona, Lista i Dane źródłowe.

- `Dane źródłowe` - zawierają parametry przyjęte przez skrypt do otwarcia plików, będące punktem wyjścia dla generowanych danych.
- `Lista` - to pełny zestaw rekordów stworzony na podstawie danych źródłowych. Kolumna "Value" przedstawia przewidywane zużycie oparte na profilu i strefie czasowej.
- `Lista scalona` - spłaszcza i grupuje wyniki z Listy według dat, sumując wartości z kolumny "Value" dla każdego dnia.
- `Tabela przestawna` - agreguje dane z Listy według godziny i daty. Komórki zawierają sumy wartości z kolumny "Value" z arkusza Lista.

## Optymalizacja wczytywania danych
Projekt Generator Danych Dobowo-Godzinowych wykorzystuje format Parquet do przechowywania danych, co zwiększa wydajność i prędkość przetwarzania dużych zbiorów danych dzięki efektywniejszej kompresji i odczytowi. Dostępne narzędzie `stwórz_parquet.py` pozwala na łatwą konwersję danych z Excela do Parquet, ułatwiając przygotowanie danych wejściowych i przyspieszając ich wczytywanie.

## Przykładowe dane wejściowe
- Profil zużycia: Plik Excel lub Parquet zawierający dane o zużyciu w różnych godzinach i dniach.
- Strefa czasowa: Plik Excel lub Parquet określający strefy czasowe dla danych profilów zużycia.
- Szablon płachty godzinowej: Plik Parquet definiujący szablon dla danych godzinowych.

### Zasada działania

Proces ten można podzielić na kilka kluczowych kroków:

- Wprowadzenie danych wejściowych: Użytkownik podaje zakres dat oraz całkowity wolumen zużycia energii w tym okresie. Zakres dat określa, które godziny zostaną wzięte pod uwagę w analizie.

- Selekcja godzin: Na podstawie podanego zakresu dat algorytm wybiera godziny, które zostaną uwzględnione w dalszych obliczeniach. Każdej godzinie przypisywane są informacje o profilu zużycia oraz strefie czasowej.

- Przypisanie profilu zużycia: Do wyselekcjonowanych godzin dołączane są dane o profilu zużycia, co pozwala na uwzględnienie zmienności zużycia energii w różnych porach dnia i w różnych okresach.

- Kalkulacja zużycia: Dla każdej godziny obliczana jest przewidywana wartość zużycia energii. Jest to robione poprzez zsumowanie wartości profilu zużycia dla danej godziny, a następnie obliczenie stosunku sumy profilu do całkowitego wolumenu zużycia. Wynik ten mnożony jest przez profil zużycia w danej godzinie, co pozwala oszacować prawdopodobne zużycie energii w tej godzinie.


### Założenia
- Całkowite zużycie energii w analizowanym okresie od 01-01-2024 do 01-02-2024: 1500 kWh.
- Suma wartości profilu zużycia dla wszystkich godzin w analizowanym okresie: 200
- Wartości profilu zużycia dla poszczególnych godzin (przykładowo dla 24 godzin): 5, 10, 15, ... (suma = 200).

$$\frac{Suma\,zużycia\,z\,zakresu}{Suma\,wartości\,profilu\,z\,zakresu} \times Wartość\,profilu\,w\,danej\,godzinie = Wartość\,zużycia\,w\,danej\,godzinie$$

- Godzina 1 - $\frac{1500\,kWh}{200} * 5 = 37,5\,kWh$
- Godzina 2 - $\frac{1500\,kWh}{200} * 10 = 75\,kWh$
- Godzina 3 - $\frac{1500\,kWh}{200} * 15 = 112,5\,kWh$
- ...

## Interfejs Graficzny (GUI)

Projekt zawiera również interfejs graficzny (GUI), który umożliwia łatwe korzystanie z funkcjonalności generatora danych dobowo-godzinowych bez konieczności bezpośredniego uruchamiania skryptów czy modyfikacji kodu. GUI jest zbudowane przy użyciu biblioteki Tkinter.

### Funkcjonalności GUI
- **Wybór pliku z danymi**: Użytkownik może wybrać plik Excel z danymi wejściowymi, który zostanie użyty do generowania danych.
- **Przetwarzanie danych**: Po wybraniu pliku, użytkownik może przetworzyć dane, uruchamiając proces generowania danych dobowo-godzinowych.
- **Wczytywanie profili i stref**: Przycisk umożliwia wczytanie aktualnych profili zużycia i stref czasowych w formacie Parquet, co jest przygotowaniem do generacji danych.
- **Informacje o postępie**: Po przetworzeniu danych, użytkownik otrzymuje informacje o sukcesie operacji lub o błędach, które wystąpiły podczas procesu.


### Zalecane użycie
GUI jest zalecane dla użytkowników, którzy preferują pracę z graficznym interfejsem użytkownika, a nie z wierszem poleceń. Zapewnia ono szybki dostęp do podstawowych funkcji projektu bez potrzeby zagłębiania się w szczegóły implementacji czy skryptów.

### Wymagania
- Python 3.6+
- Tkinter (zazwyczaj dostępny domyślnie w instalacji Pythona)
- Pandas
- OpenPyXL (dla obsługi plików Excel)
- PyArrow (dla obsługi plików Parquet)
