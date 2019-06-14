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
Graf cini 5 komponenti, pa je dijametar neizracunljiv (gigantsku komponentu cini 99.78852762357917% ukupnog broja cvorova)

Provera klasterabilnosti...
Graf je preveliki da bi se graficki prikazao

Pravljene klastera...
...napravljeni

Detektovanje koalicija...
...detektovane

U grafu se nalazi 3 kolalicija i 2 antikoalicija

Analiziranje sličnosti i razlike u strukturi koalicija i anti-koalicija...

Anti-koalicije su kohezivnije mreze
Koalicije su redje mreze od anti-koalicija
Koalicije imaju manji dijametar
Cvorovi anti-koalicija su vise distancirani u odnosu na cvorove koalicija

Prikazati sadrzaj klastera (Y/N) -> y
Klasteri koalicije (br. 3):
['6336', '3228']
['3271', '1870']
['3388', '1389']
Klasteri antikoalicije (br. 2):
['7188', '1', '160', '1028', '309', '11', ......... '5029']
['5837', '7465']

Pravljenje mreze klastera...
Analiziranje mreze klastera...

Linkova koji narusavaju klasterabilnost (balansiranost) ima: 1400 (njih treba ukloniti da bi mreza bila klasterabilna)
Prikazati ih (Y/N) -> y
('1', '7348') ('1', '7425') ('1', '7557') ......... ('5837', '7465')

Sacuvati graf u 'graphml' formatu (Y/N) -> n

Process finished with exit code 0

```
