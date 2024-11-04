import argparse
from itertools import combinations

times_full_name  = ["rano", "wieczorem"]
days_full_name   = ["poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela"]
months_full_name = ["styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", 
                    "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"]

times_option   =  ["r", "w"]
days_option    =  ["pn", "wt", "sr", "czw", "pt", "sb", "nd"]
months_option  =  ["sty", "lut", "mar", "kwi", "maj", "czer", 
                   "lip", "sie", "wrz", "paz", "lis", "gru"]

def csv_operacje(sciezki, czy_odczyt) -> bool:
    #kod dla plików w formacie csv
    return True

def json_operacje(sciezki, czy_odczyt) -> bool:
        if czy_odczyt:
        suma_sekund = 0
        for sciezka in sciezki:
            if not os.path.exists(sciezka):
                return False
            with open(sciezka, 'r', encoding='utf-8') as file:
                linie = json.load(file)
                dane = linie[1]
                if dane.startswith("A"):
                    sekundy = re.search(r'(\d+)s;', dane)
                    suma_sekund += int(sekundy.group(1))
        print(f"Suma sekund w tym zestawie ścieżek wynosi {suma_sekund}")
    else:
        for sciezka in sciezki:
            if os.path.exists(sciezka):
                return False
            data = [ "Model; Wynik; Czas;", ]
            model = random.choice([ "A", "B", "C" ])
            wynik = random.randint(0, 1001)
            czas = f"{random.randint(0, 1001)}s"
            data.append(f"{model}; {wynik}; {czas};")
            with open(sciezka, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
    return True

def generuj_strukture_plików(miesiące, dnie, pory=None):
    result = []

    #kod dopisujący do result kolejne ścieżki plików
    #zwraca None jeśli dane są niepoprawne
    
    return result

def main():
    zipl        = lambda x, y: list(zip(x, y))
    mapl        = lambda f, l: list(map(f, l))
    ranging     = lambda options: options + [x + '-' + y for x, y in  combinations(options, 2)]
    aliasing    = lambda full, alias: mapl(lambda t: "(" + t[0] + " AS '" + t[1] + "')", zipl(full, alias))

    day_ranges          = ranging(days_option)

    list_od_month_alias = aliasing(months_full_name, months_option)
    list_of_time_alias  = aliasing(times_full_name, times_option)
    list_of_day_alias   = aliasing(days_full_name, days_option)

    parser = argparse.ArgumentParser(
        description="Odczyta wartość z plików o zadanej strukturze lub je stworzy.\n" + 
                    'Kolejność plików taka jak zadana przez użytkownika.\n' +
                    'Nie należy powielać ścieżek dla pliku w tych samych podkatalogach.\n' +
                    'Nie należy odczytywać nieistniejących plików lub tworzyć już istniejących.\n' + 
                    'Jeśli jeśli nie zostaną spełnione wymogi wejścia, program będzie wstrzymany i nie zrobi zmian w strukturze.\n',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "-m", '--miesiące', nargs='+', type=str, choices=months_option, required=True, 
        help=   "Lista miesięcy do obsłużenia.\n"
                + 'Nie może być pusta. Miesiące należy podawać osobno. Mogą się powtarzać.\n'
                + f'Dopuszczone wartości dla nazwy miesięca to:\n\t{", ".join(months_option)}\n'
                + f'Struktura będzie obsługiwać odpowiednio podkatalogi o nazwach:\n\t{", ".join(months_full_name)}\n',
        metavar = ''
    )
    
    parser.add_argument(
        '-d', '--dnie', nargs='+', type=str, choices=day_ranges, required=True,
        help=  'Zakresy dni do obsłużenia dla każdego miesiąca.\n'
                + "Ma być tyle samo zakresów co miesięcy.\n"
                + f'Można podać pojedynczy dzień, gdzie dopuszczone wartości dla nazwy dnia to:\n\t{", ".join(days_option)}\n'
                + 'Można też podać zakres dni (w postaci {od którego dnia}-{do którego dnia} włącznie) dla których mają być obsłużone pliki np. pn-czw, sr-nd.\n'
                + 'Kolejność dni jak powyżej.\n'
                + f'Struktura będzie obsługiwać odpowiednio podkatalogi o nazwach:\n\t{", ".join(days_full_name)}\n',
        metavar=''    
    )

    parser.add_argument(
        '-p', '--pora', nargs='+', type=str, choices=times_option, default=None,
        help=   "Opcjonalna lista pór dnia.\n" 
                + "Nie może być pusta. Jej długość nie powinna przekraczać ilości plików do obsłużenia.\n"
                + f"Dopuszczone wartości dla nazwy pory dnia to:\n\t{', '.join(times_option)}\n"
                + f'Struktura będzie obsługiwać odpowiednio podkatalogi o nazwach:\n\t{", ".join(times_full_name)}\n'
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

    if len(args.miesiące) != len(args.dnie):
        raise argparse.ArgumentError(None, "Ma być tyle samo zakresów co miesięcy")
    
    struktura= generuj_strukture_plików(args.miesiące, args.dnie, args.pora)

    if struktura == None:
        raise argparse.ArgumentError(None, "Zbyt długa lista pór dnia lub wielokrotne podanie tej samej ścieżki")

    correct_exec = csv_operacje(struktura, args.tworzenie) if args.csv else json_operacje(struktura, args.tworzenie)

    if not correct_exec:
        raise argparse.ArgumentError(None, "Brak podanego pliku (dla odczytu) lub Podany plik już istnieje (dla tworzenia)")
        
if __name__ == '__main__':
    main()
