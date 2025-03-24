import time
import signal
import sys
import numpy as np
from colorama import Fore, Style, init

# Initialisiere colorama
init()

# Starte mit diesen Markierungen
initial_markings = [0, 3, 15, 41, 66, 95, 97, 106, 142, 152, 220, 221, 225, 242, 295, 330, 338, 354, 382, 388, 402, 415, 486, 504, 523, 546, 553, 585]

# Globale Variablen zur Speicherung des besten gefundenen Lineals
best_ruler = None
best_length = float('inf')  # Anfangslänge sehr groß setzen
found_rulers = []
iteration_count = 0  # Zähler für die Anzahl der Iterationen
max_depth = 10  # Maximale Rekursionstiefe


def is_golomb_ruler(markings):
    """
    Überprüft, ob die gegebenen Markierungen ein gültiges Golomb-Lineal bilden.
    """
    distances = set()
    for i in range(len(markings)):
        for j in range(i + 1, len(markings)):
            distance = markings[j] - markings[i]
            if distance in distances:
                return False
            distances.add(distance)
    return True


def print_colored_ruler(ruler, color=Fore.GREEN):
    """
    Gibt das Lineal in der angegebenen Farbe aus.
    """
    print(f"{color}{ruler}{Style.RESET_ALL}", flush=True)


def search_optimal_golomb_ruler():
    """
    Suche nach dem optimalen Golomb-Lineal mit einer gezielten Strategie.
    """
    global best_ruler, best_length, iteration_count
    
    def backtrack(current_markings, depth=0):
        global best_ruler, best_length, iteration_count
        
        iteration_count += 1  # Zähler erhöhen
        
        # Überprüfen, ob die aktuelle Markierung ein Golomb-Lineal ist
        if is_golomb_ruler(current_markings):
            current_length = current_markings[-1] - current_markings[0]
            if current_length < best_length:  # Wenn es eine bessere Lösung ist
                best_ruler = tuple(current_markings)
                best_length = current_length
                found_rulers.append((best_ruler, best_length))
                
                # Neue Lösung in grün anzeigen
                print(f"\n{Fore.GREEN}Neues optimales Golomb-Lineal gefunden:{Style.RESET_ALL}")
                print_colored_ruler(best_ruler, Fore.GREEN)
                print(f"{Fore.CYAN}Länge des Lineals: {best_length}{Style.RESET_ALL}", flush=True)

        # Rekursionstiefe begrenzen
        if depth >= max_depth:
            return

        # Die Suche fortsetzen und neue Markierungen hinzufügen
        last_mark = current_markings[-1]
        for next_mark in range(last_mark + 1, 600):  # Suche bis zur maximalen Länge
            if iteration_count % 100 == 0:  # Alle 100 Iterationen den Fortschritt zeigen
                print(f"{Fore.YELLOW}[Suche Tiefe {depth}] Iteration {iteration_count}:{Style.RESET_ALL} Teste {current_markings + [next_mark]}", flush=True)
            time.sleep(0.01)  # Kurze Pause für Lesbarkeit
            backtrack(current_markings + [next_mark], depth + 1)

    # Starte mit der ersten Markierung und versuche, mehr zu finden
    backtrack(initial_markings)


def signal_handler(sig, frame):
    """
    Wird aufgerufen, wenn der Benutzer Strg + C drückt.
    """
    global best_ruler, best_length
    if best_ruler:
        print(f"\n{Fore.RED}Programm manuell gestoppt.{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Letztes gefundenes bestes Golomb-Lineal:{Style.RESET_ALL}")
        print_colored_ruler(best_ruler, Fore.GREEN)
        print(f"{Fore.CYAN}Länge des Lineals: {best_length}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}Programm gestoppt. Kein Golomb-Lineal gefunden.{Style.RESET_ALL}")


# Signal-Handler für Strg + C registrieren
signal.signal(signal.SIGINT, signal_handler)

# Suche starten
print(f"{Fore.BLUE}Starte die Suche nach dem optimalen Golomb-Lineal...{Style.RESET_ALL}\n")
search_optimal_golomb_ruler()