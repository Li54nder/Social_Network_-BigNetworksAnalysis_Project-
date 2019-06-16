# <p align="center"> :computer: Projekat (Analiza Socijalnih Mreza) :computer: </p>
<br>

## Napomena

Projekat koristi sledece biblioteke koje je potrebno instalirati za nesmetan rad:
* networkx
* numpy
* scipy
* matplotlib
* ? markov-clustering


### Primer izgleda konzole nakon jednog od izvrsavanja programa
```
__main__
**********************************
*    Projekat Socijalne Mreze    *
**********************************

Izabrati ucitavanje:
>>> 1 <<< Ucitaj jednostavan gotov afinitetan graf
>>> 2 <<< Ucitaj graf iz 'graphml' formata
>>> 3 <<< Ucitaj graf iz fajla
>>> 4 <<< Generisi klasterabilan graf zadate velicine
 -> 3
Izabrati koji od ponudjenih grafova ucitati:
> 1 < Graf iz fajla 'bitcoinalpha.csv' sa 'Stanforda'
> 2 < Graf iz fajla 'wiki-RfA.txt' sa 'Stanforda'
> 3 < Graf iz fajla 'slashdot.txt' sa 'Stanforda'
 -> 1
Loading graph (1/2)...
Loading graph (2/2)...
Loading done!

Graf je ucitan i sadrzi 3783 cvorova i 14124 linkova
Broj povezanih komponenti u grafu: 5
Graf cini 5 komponenti, pa je dijametar neizracunljiv (gigantsku komponentu cini 99.79% ukupnog broja cvorova)

Provera klasterabilnosti...
Graf je preveliki da bi se graficki prikazao

Pravljene klastera...
...napravljeni

Detektovanje koalicija...
...detektovane

U grafu se nalazi 121 kolalicija i 1 antikoalicija

Analiziranje sličnosti i razlike u strukturi koalicija i anti-koalicija...

Anti-koalicije su kohezivnije mreze
Koalicije su redje mreze od anti-koalicija
Koalicije imaju manji dijametar
Cvorovi anti-koalicija su vise distancirani u odnosu na cvorove koalicija

Prikazati sadrzaj klastera (Y/N) -> y
Klasteri koalicije (br. 121):
['838']
['7534']
['7474']
['7454']
['7367']
['3271', '1870']
['7468']
........
['7547']
['1584', '6792', '527']
['7480']
........
['7451', '7452']
['7496']
['7546']
Klasteri antikoalicije (br. 1):
['7188', '1', '160', '1028', '309', '11', ........ '3296']

Pravljenje mreze klastera...
Analiziranje mreze klastera...

Linkova koji narusavaju klasterabilnost (balansiranost) ima: 1213 (njih treba ukloniti da bi mreza bila klasterabilna)
Prikazati ih (Y/N) -> y
('1', '7589') ('309', '8') ('11', '2') ........ ('7561', '2048')

Sacuvati graf u 'graphml' formatu (Y/N) -> n

Process finished with exit code 0


```
