import csv
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates  # Importer mdates for bedre håndtering av datoer

# Lister for tidspunkt og temperatur for begge filer
fil1_tidspunkt = []
fil1_temperatur = []

fil2_tidspunkt = []
fil2_temperatur = []

# Funksjon for å konvertere dato med flere formatalternativer
def parse_date(date_str):
    for fmt in ('%d.%m.%Y %H:%M', '%m/%d/%Y %I:%M:%S %p'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None  # Returner None hvis ingen formater matcher

# Les inn fil 1
with open('temperatur_trykk_met_samme_rune_time_datasett.csv.txt', 'r') as fil1:
    reader = csv.reader(fil1, delimiter=';')  # Bruk semikolon som skilletegn
    next(reader)  # Hopp over header-raden
    
    for rad in reader:
        dato_str1 = rad[2]  # Anta at dato/tid er i tredje kolonne
        
        # Sjekk om temperaturverdier er til stede
        if rad[3]:  # Bare fortsett hvis temperaturen er til stede
            # Bytt ut komma med punktum i temperaturverdien før konvertering
            temp1 = float(rad[3].replace(',', '.'))

            # Konverter datoen til datetime-objekt med riktig datoformat
            tidspunkt1 = parse_date(dato_str1)  # Bruk funksjonen for dato parsing
            
            if tidspunkt1:  # Bare legg til hvis datoen ble konvertert
                fil1_tidspunkt.append(tidspunkt1)
                fil1_temperatur.append(temp1)

# Les inn fil 2
with open('trykk_og_temperaturlogg_rune_time.csv.txt', 'r') as fil2:
    reader = csv.reader(fil2, delimiter=';')  # Bruk semikolon som skilletegn
    next(reader)  # Hopp over header-raden

    for rad in reader:
        dato_str2 = rad[0]

        if rad[4]:  # Sjekk om temperaturverdien er til stede
            temp2 = float(rad[4].replace(',', '.'))

            # Konverter datoen til datetime-objekt med riktig datoformat
            tidspunkt2 = parse_date(dato_str2)  # Bruk funksjonen for dato parsing
            
            if tidspunkt2:  # Bare legg til hvis datoen ble konvertert
                fil2_tidspunkt.append(tidspunkt2)
                fil2_temperatur.append(temp2)

# Opprett plott
plt.figure(figsize=(12, 6))  # Juster størrelsen på figuren

# Plott temperatur fra fil 1
plt.xlabel('Tidspunkt')
plt.ylabel('Temperatur (°C) - Fil 1', color='tab:blue')
plt.plot(fil1_tidspunkt, fil1_temperatur, color='tab:blue', label='Temperatur Fil 1')
plt.tick_params(axis='y', labelcolor='tab:blue')

# Plott temperatur fra fil 2
plt.plot(fil2_tidspunkt, fil2_temperatur, color='tab:green', label='Temperatur Fil 2')
plt.legend(loc='upper left')

# Formatere x-aksen for å vise datoer bedre
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y %H:%M'))  # Vis datoer i dag-måned-år time:minutt format
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))  # Vis hver time
plt.gcf().autofmt_xdate()  # Autofomater datoene for bedre lesbarhet

# Legg til tittel og vis grafen
plt.title('Temperatur over tid')
plt.tight_layout()  # Juster layout
plt.show()
