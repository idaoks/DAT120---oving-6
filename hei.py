import csv
import matplotlib.pyplot as plt
from datetime import datetime

# Funksjon for å konvertere datoer til datetime-objekter
def parse_date(date_str, fmt):
    try:
        return datetime.strptime(date_str, fmt)
    except ValueError:
        return None

# Lister for tidspunkter og temperaturer
fil1_tidspunkt = []
fil1_temperatur = []
fil2_tidspunkt = []
fil2_temperatur = []

# Les inn fil 1
with open('temperatur_trykk_met_samme_rune_time_datasett.csv.txt', 'r') as fil1:
    reader = csv.reader(fil1, delimiter=';')
    next(reader)  # Hopp over header
    for rad in reader:
        dato_str = rad[2]  # Anta at dato/tid er i tredje kolonne
        if rad[3]:  # Bare fortsett hvis temperaturen er til stede
            temperatur1 = float(rad[3].replace(',', '.'))
            tidspunkt1 = parse_date(dato_str, '%d.%m.%Y %H:%M')  # Format for fil 1
            if tidspunkt1:  # Bare legg til hvis datoen ble konvertert
                fil1_tidspunkt.append(tidspunkt1)
                fil1_temperatur.append(temperatur1)

# Les inn fil 2
with open('trykk_og_temperaturlogg_rune_time.csv.txt', 'r') as fil2:
    reader = csv.reader(fil2, delimiter=';')
    next(reader)  # Hopp over header
    for rad in reader:
        print(f"Rådata fra fil 2: {rad}")  # Skriv ut hver rad
        dato_str2 = rad[0]  # Anta at dato/tid er i første kolonne
        if rad[4]:  # Bare fortsett hvis temperaturen er til stede
            try:
                temperatur2 = float(rad[4].replace(',', '.'))
                # Oppdatert datoformat for fil 2
                tidspunkt2 = parse_date(dato_str2, '%m/%d/%Y %H:%M')  # Format for fil 2
                if tidspunkt2:  # Bare legg til hvis datoen ble konvertert
                    fil2_tidspunkt.append(tidspunkt2)
                    fil2_temperatur.append(temperatur2)
            except ValueError as e:
                print(f"Feil ved konvertering av temperatur: {e}")

# Sjekk at vi har lest inn dataene
print("Fil 1: Antall datapunkter:", len(fil1_tidspunkt))
print("Fil 2: Antall datapunkter:", len(fil2_tidspunkt))

# Opprett plott
plt.figure(figsize=(12, 6))

# Plott temperatur fra fil 1
plt.plot(fil1_tidspunkt, fil1_temperatur, label='Temperatur Fil 1', color='tab:blue')

# Plott temperatur fra fil 2
if fil2_tidspunkt and fil2_temperatur:  # Sjekk om det er data før plotting
    plt.plot(fil2_tidspunkt, fil2_temperatur, label='Temperatur Fil 2', color='tab:green')
else:
    print("Ingen data fra Fil 2 ble plottet.")

# Legg til etiketter og tittel
plt.xlabel('Tidspunkt')
plt.ylabel('Temperatur (°C)')
plt.title('Temperatur over tid')
plt.legend()
plt.xticks(rotation=45)  # Rotér x-aksen for å gjøre datoer mer lesbare
plt.tight_layout()  # Juster layout så ingenting blir avkuttet
plt.grid(True)  # Legg til rutenett for bedre lesbarhet
plt.show()
