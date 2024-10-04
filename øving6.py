import csv
import matplotlib.pyplot as plt
from datetime import datetime

# Fil 1
fil1_tidspunkt = []
fil1_temperatur = []

# Funksjon for å konvertere datoer til datetime-objekter
def parse_date(date_str):
    for fmt in ('%d.%m.%Y %H:%M', '%d/%m/%y %H:%M'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None  # Returner None hvis ingen formater matcher

# Les inn fil 1
with open('temperatur_trykk_met_samme_rune_time_datasett.csv.txt', 'r') as fil1:
    reader = csv.reader(fil1, delimiter=';')  # Bruk semikolon som skilletegn
    next(reader)  # Hopp over header
    for rad in reader:
        dato_str = rad[2]  # Anta at dato/tid er i tredje kolonne
        if rad[3]:  # Bare fortsett hvis temperaturen er til stede
            temperatur1 = float(rad[3].replace(',', '.'))  # Anta at temperaturen er i fjerde kolonne
            
            # Konverter datoen til datetime-objekt
            tidspunkt1 = parse_date(dato_str)  # Bruk funksjonen for dato parsing
            
            if tidspunkt1:  # Bare legg til hvis datoen ble konvertert
                fil1_tidspunkt.append(tidspunkt1)
                fil1_temperatur.append(temperatur1)

# Finn startdatoen for plotting
start_time = min(fil1_tidspunkt)
# Konverter datoene til antall minutter etter start
x_values = [(tid - start_time).total_seconds() / 60 for tid in fil1_tidspunkt]

# Plott temperaturen
plt.figure(figsize=(12, 6))  # Juster størrelsen på figuren
plt.plot(x_values, fil1_temperatur, label='Temperatur Fil 1', color='tab:blue')

# Legg til etiketter og tittel
plt.xlabel('Tid i minutter etter start')
plt.ylabel('Temperatur (°C)')
plt.title('Temperatur over tid')
plt.xticks(rotation=45)  # Rotér x-aksen for å gjøre datoer mer lesbare
plt.legend()
plt.tight_layout()  # Juster layout så ingenting blir avkuttet
plt.show()
