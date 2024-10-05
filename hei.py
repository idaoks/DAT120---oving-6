import csv
import matplotlib.pyplot as plt
from datetime import datetime as dt
from decimal import Decimal

# Definerer lister for SOLA VÆRSTASJON
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


# Definerer lister for UiS VÆRSTASJON
uis_tidspunkt = []
uis_temperatur = []

# Leser inn temperatur og tidspunkt fra fil 2: UiS VÆRSTASJON
with open('trykk_og_temperaturlogg_rune_time.csv.txt', 'r') as fil:
    uis = csv.reader(fil, delimiter=';')  # Bruk semikolon som skilletegn
    next(uis)  # Hopper over øverste rad
    for rad in uis:
        if rad[0]:
            try:
                # Konverterer dato/tid
                if int(rad[1]) % 60 == 0:
                    tidspunkt2 = dt.strptime(rad[0], "%m.%d.%Y %H:%M")
                    uis_tidspunkt.append(tidspunkt2)  # Lagrer tidspunktet som datetime-objekt

            except ValueError:
                print(rad[0])
                print("Ugyldig datoformat oppdaget. Stopping lesingen av filen.")
                break

        if rad[4]:  # Temperaturopplysning er i kolonne 5
            try:
                if int(rad[1]) % 60 == 0:
                # Konverterer temperatur (fjerde kolonne) til desimal og bytter ut komma med punktum
                    temperatur2 = Decimal(rad[4].replace(',', '.'))
                    uis_temperatur.append(float(temperatur2))  # Konverterer til float
            except Exception as e:
                print(f"Feil med rad {rad}, kolonne 5: {e}")


# Størrelse for plottingen i vinduet
plt.figure(figsize=(12, 6))

# Plotter temperatur fra Sola
plt.plot(sola_tidspunkt, sola_temperatur, label='Temperatur Sola', color='green')

# Plotter temperatur fra UiS
plt.plot(uis_tidspunkt, uis_temperatur, label='Temperatur UiS', color='blue')

# Grenser
plt.ylim(10, 24)  # 10 til 24 grader i y-aksen
plt.xlim(dt(2021, 6, 11, 0, 0), dt(2021, 6, 14, 0, 0))  # Datoer i x-aksen


plt.title('Sammenligning av temperaturer - SOLA og UiS')
plt.xlabel('Tidspunkt')
plt.ylabel('Temperatur (°C)')
plt.grid()
plt.legend(loc='upper left') # Oversikt av farger og navn øverst til venstre
plt.tight_layout()  # Ordner plass til begge
plt.show()
