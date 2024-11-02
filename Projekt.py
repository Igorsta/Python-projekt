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

def csv_operacje(sciezki, czy_odczyt):
    #kod dla plików w formacie csv
    pass

def json_operacje(sciezki, czy_odczyt):
    #kod dla plików w formacie json
    pass

def generuj_strukture_plików(miesiące, dnie, pory=None):
    result = []

    #kod dopisujący do result kolejne ścieżki plików
    #zwraca None jeśli dane są niepoprawne
    
    return result

def main():
    zipl        = lambda x, y: list(zip(x, y))
    ranging     = lambda options: options + [x + '-' + y for x, y in  combinations(options, 2)]
    aliasing    = lambda full, alias: list(map(lambda t: "(" + t[0] + " AS '" + t[1] + "')", zipl(full, alias)))

    day_ranges          = ranging(days_option)

    list_od_month_alias = aliasing(months_full_name, months_option)
    list_of_time_alias  = aliasing(times_full_name, times_option)
    list_of_day_alias   = aliasing(days_full_name, days_option)

    parser = argparse.ArgumentParser(
        description="Odczyta wartość z plików o zadanej strukturze, lub je stworzy. \n" + 
                    'Kolejność plików taka jak zadana przez użytkownika.' +
                    'Nie należy powielać ścieżek dla pliku w tych samych podkatalogach',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "-m", '--miesiące', nargs='+', type=str, choices=months_option, required=True, 
        help=   "Lista miesięcy do obsłużenia. Wymagany co najmniej jeden miesiąc.\n"
                + 'Miesiące należy podawać osobno. Mogą się powtarzać.\n'
                + f'Dopuszczone wartości dla nazwy miesięca to:\n\t{", ".join(months_option)}\n'
                + f'Struktura będzie obsługiwać odpowiednio podkatalogi o nazwach:\n\t{", ".join(months_full_name)}',
        metavar = ''
    )
    
    parser.add_argument(
        '-d', '--dnie', nargs='+', type=str, choices=day_ranges, required=True,
        help=  'Zakresy dni do obsłużenia dla każdego miesiąca. Ma być tyle samo zakresów co miesięcy.\n'
                +f'Można podać pojedynczy dzień, gdzie dopuszczone wartości dla nazwy dnia to:\n\t{", ".join(days_option)}\n'
                + 'Można też podać zakres dni (w postaci {od którego dnia}-{do którego dnia} włącznie) dla których mają być obsłużone pliki np. pn-czw, sr-nd.\n'
                + 'Kolejność dni jak powyżej.\n'
                + f'Struktura będzie obsługiwać odpowiednio podkatalogi o nazwach:\n\t{", ".join(days_full_name)}',
        metavar=''    
    )

    parser.add_argument(
        '-p', '--pora', nargs='+', type=str, choices=times_option, default=None,
        help=   "Opcjonalna lista pór dnia. Długość nie powinna przekraczać ilości plików do obsłużenia.\n"
                + "Można podać wartości tylko dla początkowych plików. Domyślna wartość to 'r'.\n"
                + f"Dopuszczone wartości dla nazwy pory dnia to:\n\t{', '.join(times_option)}\n"
                + f'Struktura będzie obsługiwać odpowiednio podkatalogi o nazwach:\n\t{", ".join(times_full_name)}',
        metavar=''
    )

    parser.add_argument(
        '-t', '--tworzenie', action='store_true', 
        help="Opcjonalna flaga - jeśli dodana do polecenia, pliki będą tworzone. Domyślnie pliki są odczytywane."
    )

    parser.add_argument(
        '-c', '--csv', action='store_true', 
        help="Opcjonalna flaga - jeśli dodana do polecenia, format plików będzie csv. Domyślny format plików to json."
    )

    args = parser.parse_args()
    
    struktura= generuj_strukture_plików(args.miesiące, args.dnie, args.pora)

    if args.csv:
        csv_operacje(struktura, args.tworzenie)
    else:
        json_operacje(struktura, args.tworzenie)
    
if __name__ == '__main__':
    main()