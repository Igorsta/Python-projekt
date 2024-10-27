import argparse


def csv_operacje(sciezki, czy_odczyt):
    #kod dla plików w formacie csv
    pass

def json_operacje(sciezki, czy_odczyt):
    #kod dla plików w formacie json
    pass

def generuj_strukture_plików(miesiące, dnie, czasy=None):
    result = []

    #kod dopisujący do result kolejne ścieżki plików
    
    return result

def main():
    all_months  =  ["styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", 
                    "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"]
    all_days    =  ["pn", "wt", "sr", "czw", "pt", "sb", "nd"]
    all_ranges  =  ["pn", "wt", "sr", "czw", "pt", "sb", "nd",
                    "pn-wt", "pn-sr", "pn-czw", "pn-pt", "pn-sb", "pn-nd",
                    "wt-sr", "wt-czw", "wt-pt", "wt-sb", "wt-nd",
                    "sr-czw", "sr-pt", "sr-sb", "sr-nd",
                    "czw-pt", "czw-sb", "czw-nd",
                    "pt-sb", "pt-nd",
                    "sb-nd"]
    all_times = ["r", "w"]

    parser = argparse.ArgumentParser(description="Odczyta wartość z plików o zadanej strukturze, lub je stworzy")
    
    parser.add_argument(
        '--miesiące', nargs='+', type=str, choices=all_months, required=True, 
        help=f"Lista miesięcy (w formacie {all_months})"
    )
    
    parser.add_argument(
        '--dnie', nargs='+', type=str, choices=all_ranges, required=True,
        help=f"Lista dni (w formacie {all_days}). Można podać przedział dni (np. pn-czw, pt-nd)."
    )

    parser.add_argument(
        '--czasy', nargs='*', type=str, choices=all_times, default=None,
        help=f"Opcjonalna lista czasów (w formacie {all_times}). Domyślna wartość to 'rano'."
    )

    parser.add_argument(
        '-t', '--tworzenie', action='store_true', 
        help="Opcjonalna flaga - jeśli dodana do polecenia, pliki będą tworzone. Domyślnie pliki są odczytywane"
    )

    parser.add_argument(
        '-c', '--csv', action='store_true', 
        help="Opcjonalna flaga - jeśli dodana do polecenia, format plików będzie csv. Domyślny format plików to json"
    )
    
    args = parser.parse_args()
    
    struktura= generuj_strukture_plików(args.miesiące, args.dnie, args.czasy)
    
    if args.csv:
        csv_operacje(struktura, args.tworzenie)
    else:
        json_operacje(struktura, args.tworzenie)
    
if __name__ == '__main__':
    main()