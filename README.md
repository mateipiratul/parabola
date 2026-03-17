# Algoritmi Genetici

Implementați un **algoritm genetic** pentru determinarea **maximului** unei funcții pozitive pe un domeniu dat. Funcția va fi un polinom de gradul 2, cu coeficienți dați. Algoritmul trebuie să cuprindă etapele de **selecție**, **încrucișare** (*crossover*) și **mutație**.

## 1. Precizări

Se vor folosi metoda de codificare discutată la curs și încrucișarea cu un singur punct de tăietură/de rupere. Se va ține cont și de selecția de tip elitist (individul cu fitness-ul cel mai mare va trece automat în generația următoare).


## 2. Date de intrare

* Dimensiunea populației *(numărul de cromozomi)*
* Domeniul de definiție al funcției *(capetele unui interval închis)*
* Parametrii pentru funcția de maximizat *(coeficienții polinomului de grad 2)*
* Precizia cu care se lucrează *(cu care se discretizează intervalul)*
* Probabilitatea de recombinare *(crossover, încrucișare)*
* Probabilitatea de mutație
* Numărul de etape al algoritmului


## 3. Date de Ieșire
* Un fișier text sugestiv care prezintă detaliat operațiile efectuate **în prima etapă** a algoritmului, iar apoi un rezumat al evoluției populației pentru celelalte etape.
> 
> **Exemplu de configurare:** Pentru funcția $-x^{2}+x+2$ pe domeniul $[-1, 2]$, cu o populație de 20 indivizi, precizie 6, probabilitate de recombinare 25%, mutație 1% și 50 de etape. 
> 
> 
* **Extra:** o interfață grafică sugestivă, care afișează evoluția algoritmului.

### Conținutul fișierului de ieșire:
În fișier vor fi incluse cel puțin următoarele informații:

* **Populația inițială**, cu următoarele date pentru fiecare individ *i*:
    - $B_{i}$: reprezentarea pe biți a cromozomului;
    - $X_{i}$: valoarea corespunzătoare cromozomului în domeniul de definiție al funcției (număr real);
    - $f(X_{i})$: valoarea cromozomului, adică valoarea funcției în punctul din domeniu care corespunde acestuia.

* **Probabilități de selecție** pentru fiecare cromozom: $p_{i}=\frac{f(X_{i})}{\sum_{j}f(X_{j})}$

*  **Probabilități cumulate** care dau intervalele pentru selecție: $q_{0}=0$ $q_{i}=\sum_{j=1}^{i}p_{j}$

* **Mecanism:** Generarea unui număr aleator $u \in [0, 1)$ și determinarea intervalului $[q_{i}, q_{i+1})$ prin **căutare binară**. 


* Evidențierea procesului de selecție, care constă în generarea unui număr aleator $u \in [0, 1)$ și determinarea intervalului $[q_{i}, q_{i+1})$ căruia aparține acest număr; corespunzător acestui interval se va selecta cromozomul *$i+1$*. Procesul se repetă până se selectează numărul dorit de cromozomi.

**Cerință:** căutarea intervalului corespunzător se va face folosind căutarea binară.

* Evidențierea cromozomilor care participă la recombinare.

* Pentru recombinările caare au loc se evidențiază perechile de cromozomi care participă la recombinare, punctul de rupere generat aleator precum și cromozomii rezultați în urma recombinării *(sau, după caz, se evidențiază tipul de încrucișare ales)*.

* Populația rezultată după recombinare.

* Populația rezultată după mutațiile aleatoare.

* Pentru restul generațiilor (populațiile din etapele următoare) se va afișa doar **valoarea maximă** și **valoarea medie** a fitness-ului *(performanței)* populației:

$Max Fitness := max_{i}f(X_{i}), i \in \overline{1,\dots,n}$

$Mean Fitness := \frac{1}{n} \sum_{i = 1}^{n}{f(X_{i})}$

---
