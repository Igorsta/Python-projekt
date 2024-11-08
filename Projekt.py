from itertools import combinations
from itertools import zip_longest
from typing import List, Optional
import argparse
import random
import json
import csv
import os

typ_pliku = "json"

PORY = dict({'r':'rano', 'w': 'wieczorem'})

DNIE  = dict({"pn": "poniedziałek", "wt": "wtorek", "sr": "środa", 
                "czw": "czwartek", "pt": "piątek", "sb":"sobota", "nd":"niedziela"})

MIESIĄCE= dict({"sty":"styczeń", "lut":"luty", "mar":"marzec", "kwi":"kwiecień", 
                "maj":"maj", "czer":"czerwiec", "lip":"lipiec", "sie":"sierpień", 
                "wrz":"wrzesień", "paz":"październik", "lis":"listopad", "gru":"grudzień"})

def operacja_odczyt(sciezkaKatalogu: str) -> int:
    suma_czasu = 0
    
    sciezkaPliku = os.path.join(sciezkaKatalogu, f'Dane.{typ_pliku}')
    if not os.path.exists(sciezkaPliku):
        raise FileNotFoundError(f"{sciezkaPliku} Plik nie istnieje!")
    
    with open(sciezkaPliku, 'r', encoding='utf-8') as file:
        if typ_pliku == 'csv':
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                if row['Model'] == 'A':
                    suma_czasu += int(row['Czas'].strip('s'))

        if typ_pliku == 'json':
            dane = json.load(file)
            if dane['Model'] == 'A':
                suma_czasu += int(dane['Czas'].strip('s'))

    print(sciezkaKatalogu.ljust(65), f"odczytano Dane.{typ_pliku}".center(30),  f"ilość sekund to {suma_czasu}".rjust(10))
    
    return suma_czasu

def operacja_tworzenie(sciezkaKatalogu: str) -> None:
    os.makedirs(sciezkaKatalogu, exist_ok=True)
    
    sciezkaPliku = os.path.join(sciezkaKatalogu, f'Dane.{typ_pliku}')
    
    if os.path.exists(sciezkaPliku):
        raise FileExistsError(f"{sciezkaPliku} Plik już istnieje!")
    
    with open(sciezkaPliku, 'w', encoding='utf-8') as plik:
        if typ_pliku == 'csv':
            writer = csv.writer(plik, delimiter=';')
            writer.writerow(['Model', 'Wynik', 'Czas'])
            writer.writerow([random.choice(['A', 'B', 'C']), random.randint(0, 1000), f"{random.randint(0, 1000)}s"])
        
        if typ_pliku == "json":
            dane = {
                'Model': random.choice(['A', 'B', 'C']),
                'Wynik': random.randint(0, 1000),
                'Czas': f"{random.randint(0, 1000)}s"
            }
            json.dump(dane, plik, ensure_ascii=False, indent=4)
    
    print(sciezkaKatalogu.ljust(65), f"stworzono Dane.{typ_pliku}".center(30))
    
    return None

def generuj_strukturę_plików(miesiące: List[str], dnie: List[str], pory: List[str]) -> Optional[List[str]]:
    if pory == None:
        pory = []
    
    struktura = []
    skróty = list(DNIE.keys())

    for dzień, miesiąc, pora in zip_longest(dnie, miesiące, pory, fillvalue='r'):
        zakres = [dzień]
        
        if '-' in dzień:
            start, koniec = [skróty.index(brzeg) for brzeg in dzień.split('-')]
            zakres = skróty[start:koniec+1]
        
        for dzień in zakres:
            folder_path = os.path.join(os.getcwd(),
                                       MIESIĄCE[miesiąc],
                                       DNIE[dzień],
                                       PORY[pora])
            struktura.append(folder_path)

    if len(struktura) != len(set(struktura)):
        return None

    return struktura

def main():
    miesiące_opcje  = list(MIESIĄCE.keys())
    dnie_opcje      = list(DNIE.keys())
    pory_opcje      = list(PORY.keys())

    miesiące_pełne_nazwy= list(MIESIĄCE.values())
    pory_pełne_nazwy    = list(PORY.values())
    dnie_pełne_nazwy    = list(DNIE.values())

    zakresy_dni  = dnie_opcje + [x + '-' + y for x, y in  combinations(dnie_opcje, 2)]

    parser = argparse.ArgumentParser(
        description="Odczyta wartość z plików o zadanej strukturze lub je stworzy.\n" + 
                    'Kolejność plików taka jak zadana przez użytkownika.\n' +
                    'Nie należy powielać ścieżek dla pliku w tych samych podkatalogach.\n' +
                    'Nie należy odczytywać nieistniejących plików lub tworzyć już istniejących.\n' + 
                    'Jeśli jeśli nie zostaną spełnione wymogi, program przerwie wykonywanie i nie dokończy odczytywania/tworzenia plików.\n',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "-m", '--miesiące', nargs='+', type=str, choices=miesiące_opcje, required=True, 
        help=   "Lista miesięcy do obsłużenia.\n"
                + 'Nie może być pusta. Miesiące należy podawać osobno. Mogą się powtarzać.\n'
                + f'Dopuszczone wartości dla nazwy miesięca to:\n\t{", ".join(miesiące_opcje)}\n'
                + f'Program będzie obsługiwać odpowiednio podkatalogi o nazwach:\n\t{", ".join(miesiące_pełne_nazwy)}\n',
        metavar = ''
    )
    
    parser.add_argument(
        '-d', '--dnie', nargs='+', type=str, choices=zakresy_dni, required=True,
        help=  'Zakresy dni do obsłużenia dla każdego miesiąca.\n'
                + "Ma być tyle samo zakresów co miesięcy.\n"
                + f'Można podać pojedynczy dzień, gdzie dopuszczone wartości dla nazwy dnia to:\n\t{", ".join(dnie_opcje)}\n'
                + 'Można też podać zakres dni (w postaci {od którego dnia}-{do którego dnia} włącznie)\ndla których mają być obsłużone pliki np. pn-czw, sr-nd.\n'
                + 'Kolejność dni jak powyżej.\n'
                + f'Struktura będzie obsługiwać odpowiednio podkatalogi o nazwach:\n\t{", ".join(dnie_pełne_nazwy)}\n',
        metavar=''    
    )

    parser.add_argument(
        '-p', '--pora', nargs='+', type=str, choices=pory_opcje, default=None,
        help=   "Opcjonalna lista pór dnia.\n" 
                + "Nie może być pusta. Jej długość nie może przekraczać liczby miesięcy\n"
                + f"Dopuszczone wartości dla nazwy pory dnia to:\n\t{', '.join(pory_opcje)}\n"
                + f'Struktura będzie obsługiwać odpowiednio podkatalogi o nazwach:\n\t{", ".join(pory_pełne_nazwy)}\n'
                + "Można podać wartości tylko dla początkowych plików. Domyślna wartość to 'r'.\n",
        metavar=''
    )

    parser.add_argument(
        '-t', '--tworzenie', action='store_true', 
        help=   "Opcjonalna flaga.\n"
                + "Jeśli dodana do polecenia, pliki będą tworzone.\n"
                + "Domyślnie pliki są odczytywane.\n"
    )

    parser.add_argument(
        '-c', '--csv', action='store_true', 
        help=   "Opcjonalna flaga.\n"
                + "Jeśli dodana do polecenia, format plików będzie csv.\n"
                + "Domyślny format plików to json.\n"
    )

    arg = parser.parse_args()

    if len(arg.miesiące) != len(arg.dnie):
        raise argparse.ArgumentError(None, "Ma być tyle samo zakresów co miesięcy")
    
    if arg.pora != None and len(arg.pora) > len(arg.miesiące):
        raise argparse.ArgumentError(None, "Podano za dużo pór")
    
    struktura= generuj_strukturę_plików(arg.miesiące, arg.dnie, arg.pora)

    if struktura == None:
        raise argparse.ArgumentError(None, "Wielokrotne podano tą samą ścieżkę")

    if arg.csv == True:
        global typ_pliku
        typ_pliku = "csv" 

    suma_sekund = 0

    for sciezka in struktura:
        try:
            if arg.tworzenie:
                operacja_tworzenie(sciezka)
            else:
                suma_sekund += operacja_odczyt(sciezka)

        except Exception as e:
            raise Exception (f'Obsługa zapytania zakończyła się błędem {e}')

    if not arg.tworzenie:
        print(f"Łączna suma sekund dla modelu A: {suma_sekund}s")

if __name__ == '__main__':
    main()