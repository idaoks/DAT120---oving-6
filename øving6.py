import csv
import matplotlib.pyplot as plt
from datetime import datetime as dt
from decimal import Decimal

# Definerer lister for fil 1: SOLA VÆRSTASJON
sola_tidspunkt = []
sola_temperatur = []

# Leser inn temperatur og tidspunkt fra fil 1: SOLA VÆRSTASJON
with open('temperatur_trykk_met_samme_rune_time_datasett.csv.txt', 'r') as fil:
    sola = csv.reader(fil, delimiter=';')  # Bruk semikolon som skilletegn
    next(sola)  # Hopper over øverste rad
    for rad in sola:
        if rad[2] and rad[3]:
            try:
                # Konverterer dato/tid (tredje kolonne)
                tidspunkt1 = dt.strptime(rad[2], "%d.%m.%Y %H:%M")
                sola_tidspunkt.append(tidspunkt1)  # Lagrer tidspunktet som datetime-objekt

                # Konverterer temperatur (fjerde kolonne) til desimal og bytter ut komma med punktum
                temperatur1 = Decimal(rad[3].replace(',', '.'))
                sola_temperatur.append(float(temperatur1))  # Konverterer til float

            except Exception as e:
                print(f"Feil med rad {rad}: {e}")

# Plotting av temperaturen mot tid
plt.figure(figsize=(12, 6))  # Setter figurstørrelse
plt.plot(sola_tidspunkt, sola_temperatur)
plt.title('Temperatur over tid')
plt.xlabel('Tidspunkt')
plt.ylabel('Temperatur (°C)')
plt.xticks(rotation=45)  # Roterer x-aksen for bedre lesbarhet
plt.grid()
plt.tight_layout()  # Sørger for at alt får plass
plt.figlegend()
plt.show()



"""
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
"""