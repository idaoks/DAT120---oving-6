import csv
import matplotlib.pyplot as plt
from datetime import datetime as dt
from decimal import Decimal

# Funksjon for å beregne gjennomsnitt
def beregn_gjennomsnitt(tidspunkt_liste, temperatur_liste, n):
    gyldige_tidspunkt = []
    gjennomsnitt_temperatur = []

    for i in range(n, len(temperatur_liste)):
        snitt = sum(temperatur_liste[i-n:i]) / n
        gyldige_tidspunkt.append(tidspunkt_liste[i])
        gjennomsnitt_temperatur.append(snitt)
    
    return gyldige_tidspunkt, gjennomsnitt_temperatur

# Definerer lister for SOLA VÆRSTASJON:
sola_tidspunkt = []
sola_temperatur = []
sola_trykk = []

# Leser inn temperatur og trykk fra SOLA filen
with open('temperatur_trykk_met_samme_rune_time_datasett.csv.txt', 'r') as fil:
    sola = csv.reader(fil, delimiter=';')
    next(sola)  # Hopper over headeren
    for rad in sola:
        if rad[2] and rad[3] and rad[4]:  # Sjekk at alle verdiene er til stede
            try:
                tidspunkt1 = dt.strptime(rad[2], "%d.%m.%Y %H:%M")
                sola_tidspunkt.append(tidspunkt1)
                temperatur1 = Decimal(rad[3].replace(',', '.'))
                sola_temperatur.append(float(temperatur1))
                trykk1 = Decimal(rad[4].replace(',', '.'))
                sola_trykk.append(float(trykk1))
            except Exception as e:
                print(f"Feil med rad {rad}: {e}")

# Definerer lister for UiS VÆRSTASJON:
uis_tidspunkt = []
uis_temperatur = []
uis_absolutt_trykk = []
uis_barometrisk_trykk = []

# Leser inn data fra UiS filen
with open('trykk_og_temperaturlogg_rune_time.csv.txt', 'r') as fil:
    uis = csv.reader(fil, delimiter=';')
    next(uis)  # Hopper over headeren
    for rad in uis:
        if rad[0] and rad[4] and rad[2] and rad[3]:
            try:
                tidspunkt2 = dt.strptime(rad[0], "%m.%d.%Y %H:%M")
                uis_tidspunkt.append(tidspunkt2)
                temperatur2 = Decimal(rad[4].replace(',', '.'))
                uis_temperatur.append(float(temperatur2))
                trykk_absolutt = Decimal(rad[2].replace(',', '.'))
                uis_absolutt_trykk.append(float(trykk_absolutt))
                trykk_barometrisk = Decimal(rad[3].replace(',', '.'))
                uis_barometrisk_trykk.append(float(trykk_barometrisk))
            except Exception as e:
                print(f"Feil med rad {rad}: {e}")

# Plotting i ett vindu med flere subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Temperaturplott (øverste subplot)
ax1.plot(sola_tidspunkt, sola_temperatur, label='Temperatur Sola', color='green')
ax1.plot(uis_tidspunkt, uis_temperatur, label='Temperatur UiS', color='blue')

# Beregn og plot gjennomsnittstemperatur (n=30)
n = 30
sola_gyldige_tidspkt, sola_gjennomsnitt = beregn_gjennomsnitt(sola_tidspunkt, sola_temperatur, n)
uis_gyldige_tidspkt, uis_gjennomsnitt = beregn_gjennomsnitt(uis_tidspunkt, uis_temperatur, n)
ax1.plot(sola_gyldige_tidspkt, sola_gjennomsnitt, label='Gjennomsnitt Sola (n=30)', color='orange')
ax1.plot(uis_gyldige_tidspkt, uis_gjennomsnitt, label='Gjennomsnitt UiS (n=30)', color='red')

# Temperaturfall fra 11. juni kl. 17:31 til 12. juni kl. 03:05
start_tid = dt(2021, 6, 11, 17, 31)
slutt_tid = dt(2021, 6, 12, 3, 5)
start_indeks = next(i for i, t in enumerate(sola_tidspunkt) if t >= start_tid)
slutt_indeks = next(i for i, t in enumerate(sola_tidspunkt) if t >= slutt_tid)
ax1.plot(sola_tidspunkt[start_indeks:slutt_indeks], sola_temperatur[start_indeks:slutt_indeks], label='Temperaturfall Sola', color='purple')

ax1.set_title('Temperaturer - Sola og UiS')
ax1.set_xlabel('Tidspunkt')
ax1.set_ylabel('Temperatur (°C)')
ax1.legend(loc='upper left')
ax1.grid()

# Trykkplott (nederste subplot)
ax2.plot(sola_tidspunkt, sola_trykk, label='Lufttrykk Sola', color='red')
ax2.plot(uis_tidspunkt, uis_absolutt_trykk, label='Absolutt trykk UiS', color='blue')
ax2.plot(uis_tidspunkt, uis_barometrisk_trykk, label='Barometrisk trykk UiS', color='cyan')

ax2.set_title('Trykk - Sola og UiS')
ax2.set_xlabel('Tidspunkt')
ax2.set_ylabel('Trykk')
ax2.legend(loc='upper left')
ax2.grid()

plt.tight_layout()
plt.show()
