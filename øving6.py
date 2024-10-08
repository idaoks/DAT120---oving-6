import csv
import matplotlib.pyplot as plt
from datetime import datetime as dt
from decimal import Decimal
import numpy as np

# Definerer lister for SOLA VÆRSTASJON:
sola_tidspunkt = []
sola_temperatur = []

sola_tidspunkt_abstrykk = []
sola_absolutt_trykk = []

# Leser inn temperatur og tidspunkt fra fil 1: SOLA VÆRSTASJON
with open('temperatur_trykk_met_samme_rune_time_datasett.csv.txt', 'r') as fil:
    sola = csv.reader(fil, delimiter=';')  # I CSV filen brukes semikolon som skilletegn
    next(sola)  # Hopper over øverste rad
    for rad in sola:
        if rad[2] and rad[3]: # Hvis det eksisterer en verdi i både kolonne 3 og 4
            try:
                # Henter tidspunkt, konverterer og legger i liste (Viktig: lagres som datetime objekt)
                tidspunkt1_temperatur = dt.strptime(rad[2], "%d.%m.%Y %H:%M")
                sola_tidspunkt.append(tidspunkt1_temperatur)

                # Konverterer temperatur (fjerde kolonne) til desimal og bytter ut komma med punktum
                temperatur1 = Decimal(rad[3].replace(',', '.'))
                sola_temperatur.append(float(temperatur1)) 
            
            # Bruker en try-except blokk i hver rad for å lettere finne feilkilder hvis koden feiler.
            except Exception as e:
                print(f"(ABSOLUTT TRYKK): Feil med rad {rad}: {e}")
            
        # Tilsvarende for å hente absolutt trykk:
        if rad[2] and rad[4]:
            try:
                absolutt_trykk1 = Decimal(rad[4].replace(',','.'))
                sola_absolutt_trykk.append(float(absolutt_trykk1))
            
            # Bruker en try-except blokk i hver rad for å lettere finne feilkilder hvis koden feiler.
            except Exception as e:
                print(f"(ABSOLUTT TRYKK): Feil med rad {rad}: {e}")


# Definerer lister for UiS VÆRSTASJON:
uis_tidspunkt = []
uis_temperatur = []

uis_absolutt_trykk = []
uis_absolutt_trykk_tid = []

uis_barometrisk_trykk = []
uis_barometrisk_trykk_tid = []

# Leser inn data fra fil 2: UiS VÆRSTASJON
with open('trykk_og_temperaturlogg_rune_time.csv.txt', 'r') as fil:
    uis = csv.reader(fil, delimiter=';')  # Semikolon er skilletegn her også
    next(uis)  # Hopper over øverste rad
    for rad in uis:
        if rad[0]:
            try:
                # Konverterer dato/tid
                if int(rad[1]) % 60 == 0:
                    tidspunkt2 = dt.strptime(rad[0], "%m.%d.%Y %H:%M")
                    uis_tidspunkt.append(tidspunkt2)  # Lagrer tidspunktet som datetime-objekt

            except ValueError: # Bruker except ValueError for å stoppe når datoformat endres 2/3 ut i fila.
                print(rad[0])
                print("Ugyldig datoformat oppdaget. Stopping lesingen av filen.")
                break

        if rad[4]: # Temperatur er i kolonne 5
            try:
                if int(rad[1]) % 60 == 0: # Hvis resten av regnestykket (sekunder)/60 er lik 0 (for å filtrere hver 6. måling).
                    temperatur2 = Decimal(rad[4].replace(',', '.'))
                    uis_temperatur.append(float(temperatur2))

            except Exception as e: # Bruker exception til å lettere finne feilkilder
                print(f"Feil med rad {rad}, kolonne 5: {e}")
        
        if rad[3]:
            try:
                if int(rad[1]) % 60 == 0:
                    absolutt_trykk2 = Decimal(rad[3].replace(',','.'))
                    uis_absolutt_trykk.append(float(absolutt_trykk2) * 10)
            
            except Exception as e:
                print(f"(ABSOLUTT TRYKK UIS): Feil med rad {rad}, kolonne 5: {e}")
        
        if rad[2]:
            try:
                if int(rad[1]) % 60 == 0:
                    barometrisk_trykk2 = Decimal(rad[2].replace(',','.'))
                    uis_barometrisk_trykk.append(float(barometrisk_trykk2) * 10)
            
            except Exception as e:
                print(f"(BAROMETRISK TRYKK UIS): Feil med rad {rad}, kolonne 5: {e}")


# g) Funksjon som regner "glidegjennomsnitt"
def gjsnitt(tider=list, temperaturer=list, n=int):
            """ Tar inn tre inputs: liste med tider, liste med temperaturer og et tall n. """
            # Definerer lister som skal fylles opp:
            gyldige_tidspunkt = [] # Liste som vil lagre alle tidspunktene hvor det fins n tidligere og senere målinger.
            gjsnitt_temperatur = [] # Liste som vil lagre gjennomsnittet av de siste og neste n målingene ved hvert gyldige tidspunkt
            
            # Går gjennom alle tidspunkt og temperaturer:
            for i in range(n, len(temperaturer) - n):  # Starter på indeks n i lista (fordi vi må ha minst n målinger allerede for å se på de n forrige), og fortsetter til lengden av listen er n målinger før temperaturen er ferdig (siden vi også skal se på de 30 neste målingene).
                snitt = sum(temperaturer[i-n : i + n + 1]) / (2 * n + 1) # Sum av temperaturer fra n verdier FØR nåværende verdi (i-n) til n verdier ETTER nåværende verdi (i+n). Bruk av ":" kalles slicing. Deler på antallet, 1 + 2*n.
                
                # Nå har vi gyldige tidspunkter og gjennomsnittstemperaturene kan vi legge dem til i listene:
                gyldige_tidspunkt.append(tider[i])
                gjsnitt_temperatur.append(snitt)
            
            # Returnerer de ferdige listene
            return gyldige_tidspunkt, gjsnitt_temperatur

# Definerer n, hvor langt fram og tilbake vi vil gå fra hver verdi.
n = 30

# Finner x- og y-verdier for glidegjennomsnittet for verdien n, og erklærer det i variabler.
gyldige_tidspunkt, gjsnitt_temperatur = gjsnitt(uis_tidspunkt, uis_temperatur, n)


# h) Finn temperaturfall mellom 11. juni kl 17:31 og 12. juni kl 03:05

# Definerer tider for start og slutt:
start_tid = dt(2021, 6, 11, 17, 31)
slutt_tid = dt(2021, 6, 12, 3, 5)

# Definerer funksjon som finner indeksen til et tidspunkt:
def finn_indeks(tidspunktliste=list, gitt_tidspunkt=dt):
    """
    En funksjon som tar inn en liste tider og et mål-tidspunkt.
    Finner indeksen til et det gitte gitt tidspunkt i listen.
    """
    for i in range(len(tidspunktliste)): 
        if tidspunktliste[i] >= gitt_tidspunkt: # Når vi finner ut at tidspunktet i listen er lik eller større som måø, så returnerer
            return i # Returnerer riktig index
    return -1 # Returnerer siste tidspunkt hvis ingen passer
# Finner når i tidspunkt-listen til UiS fila at vi finner start- og slutt-tidene:
start_indeks = finn_indeks(uis_tidspunkt, start_tid)
slutt_indeks = finn_indeks(uis_tidspunkt, slutt_tid)

# Henter tidspunkt og temperaturer mellom indeksene vi fant:
kveld_tidspunkt = uis_tidspunkt[start_indeks:slutt_indeks+1]
kveld_temperatur = uis_temperatur[start_indeks:slutt_indeks+1]


# i) Plott atmosferisk trykk fra begge filene sammen med barometrisk trykk.



# Plotter temperaturer og trykk som subplotter
print(f"Lengde på uis_barometrisk_trykk: {len(uis_barometrisk_trykk)}")
print(f"Første 5 elementer i uis_absolutt_trykk: {uis_barometrisk_trykk[:5]}")


fig, (temperatur, trykk) = plt.subplots(2, 1, figsize=(8, 10))

# Første subplot for temperaturer
temperatur.plot(sola_tidspunkt, sola_temperatur, label='Temperatur Sola', color='green')
temperatur.plot(uis_tidspunkt, uis_temperatur, label='Temperatur UiS', color='blue')
temperatur.plot(gyldige_tidspunkt, gjsnitt_temperatur, label=f'Gjennomsnitt UiS for n={n}', color='orange')
temperatur.plot([kveld_tidspunkt[0], kveld_tidspunkt[-1]], [kveld_temperatur[0], kveld_temperatur[-1]], label='Temperaturfall 11-12 juni UiS', color='purple')

temperatur.set_ylim(10, 24)
temperatur.set_xlim(dt(2021, 6, 11, 0, 0), dt(2021, 6, 14, 0, 0))
temperatur.set_title('Sammenligning av temperaturer - SOLA og UiS')
temperatur.set_xlabel('Tidspunkt')
temperatur.set_ylabel('Temperatur (°C)')
temperatur.grid()
temperatur.legend(loc='upper left')

# Andre subplot for absolutt trykk fra Sola
trykk.plot(sola_tidspunkt, sola_absolutt_trykk, label='Absolutt Trykk Sola', color='green')
trykk.plot(uis_tidspunkt, uis_absolutt_trykk, label='Absolutt trykk UiS', color='blue')
trykk.plot(uis_tidspunkt, uis_barometrisk_trykk, label='Barometrisk trykk UiS', color='orange')

trykk.set_ylim(1000, 1025)
trykk.set_xlim(dt(2021, 6, 11, 0, 0), dt(2021, 6, 14, 0, 0))
trykk.set_title('Absolutt Trykk - Sola Værstasjon')
trykk.set_xlabel('Tidspunkt')
trykk.set_ylabel('Trykk')
trykk.grid()
trykk.legend(loc='upper left')

plt.subplots_adjust(hspace=0.4)  # Øker avstanden mellom subplottene
plt.tight_layout()
plt.show()
