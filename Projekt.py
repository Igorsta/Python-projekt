from itertools import combinations
from itertools import zip_longest
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


def utworz_plik_csv(sciezka):
    """
    Tworzy plik CSV w podanej ścieżce z przykładowymi danymi.
    """
    if not os.path.exists(sciezka):
        os.makedirs(sciezka)
    
    file_path = os.path.join(sciezka, 'Dane.csv')
    if os.path.exists(file_path):
        return False  # Plik już istnieje, nie tworzymy ponownie

    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['Model', 'Wynik', 'Czas'])
        writer.writerow([random.choice(['A', 'B', 'C']), random.randint(0, 1000), f"{random.randint(0, 1000)}s"])

    return True

def utworz_plik_json(sciezka):
    """
    Tworzy plik JSON w podanej ścieżce z przykładowymi danymi.
    """
    if not os.path.exists(sciezka):
        os.makedirs(sciezka)
    
    file_path = os.path.join(sciezka, 'Dane.json')
    if os.path.exists(file_path):
        return False  # Plik już istnieje, nie tworzymy ponownie

    data = {
        'Model': random.choice(['A', 'B', 'C']),
        'Wynik': random.randint(0, 1000),
        'Czas': f"{random.randint(0, 1000)}s"
    }

    with open(file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

    return True

def odczyt_plik_csv(sciezka):
    """
    Odczytuje plik CSV i sumuje wartości 'Czas' dla wierszy, w których 'Model' to 'A'.
    """
    suma_czasu = 0

    file_path = os.path.join(sciezka, 'Dane.csv')
    if not os.path.exists(file_path):
        return False  # Plik nie istnieje

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if row['Model'] == 'A':
                suma_czasu += int(row['Czas'].strip('s'))

    return suma_czasu

def odczyt_plik_json(sciezka):
    """
    Odczytuje plik JSON i sumuje wartości 'Czas' dla wierszy, w których 'Model' to 'A'.
    """
    suma_czasu = 0

    file_path = os.path.join(sciezka, 'Dane.json')
    if not os.path.exists(file_path):
        return False  # Plik nie istnieje

    with open(file_path, 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
        if data['Model'] == 'A':
            suma_czasu += int(data['Czas'].strip('s'))

    return suma_czasu

def generuj_strukture_plików(miesiące, dnie, pory, czy_csv):
    if pory == None:
        pory = []
    
    struktura = []
    shortcut = list(DNIE.keys())

    for dzień, miesiąc, pora in zip_longest(dnie, miesiące, pory, fillvalue='r'):
        zakres = [dzień]
        
        if '-' in dzień:
            start, end = [shortcut.index(brzeg) for brzeg in dzień.split('-')]
            zakres = shortcut[start:end+1]
        
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
    miesiące_opcje= list(MIESIĄCE.keys())
    pory_opcje = list(PORY.keys())
    dni_opcje  = list(DNIE.keys())

    miesiące_pełne_nazwy= list(MIESIĄCE.values())
    pory_pełne_nazwy = list(PORY.values())
    dni_pełne_nazwy  = list(DNIE.values())

    zakresy_dni  = dni_opcje + [x + '-' + y for x, y in  combinations(dni_opcje, 2)]

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
                + f'Można podać pojedynczy dzień, gdzie dopuszczone wartości dla nazwy dnia to:\n\t{", ".join(dni_opcje)}\n'
                + 'Można też podać zakres dni (w postaci {od którego dnia}-{do którego dnia} włącznie)\ndla których mają być obsłużone pliki np. pn-czw, sr-nd.\n'
                + 'Kolejność dni jak powyżej.\n'
                + f'Struktura będzie obsługiwać odpowiednio podkatalogi o nazwach:\n\t{", ".join(dni_pełne_nazwy)}\n',
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

    args = parser.parse_args()

    if len([args.miesiące]) != len([args.dnie]):
        raise argparse.ArgumentError(None, "Ma być tyle samo zakresów co miesięcy")
    
    if len([args.pora]) > len([args.miesiące]):
        raise argparse.ArgumentError(None, "Podano za dużo pór")
    
    struktura= generuj_strukture_plików(args.miesiące, args.dnie, args.pora, args.csv)

    if struktura == None:
        raise argparse.ArgumentError(None, "Wielokrotne podano tą samą ścieżkę")

    if args.csv == True:
        global typ_pliku
        typ_pliku = "csv" 

    suma_sekund = 0

    for sciezka in struktura:
        
        sciezkaDoPlik = os.path.join(sciezka, f"plik.{typ_pliku}")

        if args.tworzenie == os.path.exists(sciezkaDoPlik):
            raise argparse.ArgumentError(None, f"Problem z dostępem do pliku! {sciezkaDoPlik}")

        try:
            if args.tworzenie:
                if args.csv:
                    utworz_plik_csv(sciezka)
                else:
                    utworz_plik_json(sciezka)
            else:
                if args.csv:
                    odczyt_plik_csv(sciezka)
                else:
                    odczyt_plik_json(sciezka)

        except Exception as e:
            raise Exception (f'Obsługa zapytania zakończyła się błędem {e}')

    if not args.tworzenie:
        print(f"Łączna suma sekund dla modelu A: {suma_sekund}s")

if __name__ == '__main__':
    main()
