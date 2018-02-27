## Ejercicio 1

### Estadísticas:

Basic Statistics
================
sents: 17378
tokens: 517194
words: 46501
tags: 85

Most Frequent POS Tags
======================
tag	freq	%	top
sp000	79884	15.45	(de, en, a, del, con)
nc0s000	63452	12.27	(presidente, equipo, partido, país, año)
da0000	54549	10.55	(la, el, los, las, El)
aq0000	33906	6.56	(pasado, gran, mayor, nuevo, próximo)
fc	30147	5.83	(,)
np00000	29111	5.63	(Gobierno, España, PP, Barcelona, Madrid)
nc0p000	27736	5.36	(años, millones, personas, países, días)
fp	17512	3.39	(.)
rg	15336	2.97	(más, hoy, también, ayer, ya)
cc	15023	2.90	(y, pero, o, Pero, e)

Word Ambiguity Levels
=====================
n	words	%	top
1	43972	94.56	(,, con, por, su, El)
2	2318	4.98	(el, en, y, ", los)
3	180	0.39	(de, la, ., un, no)
4	23	0.05	(que, a, dos, este, fue)
5	5	0.01	(mismo, cinco, medio, ocho, vista)
6	3	0.01	(una, como, uno)
7	0	0.00	()
8	0	0.00	()
9	0	0.00	()


## Ejercicio 2

### Resultados obtenidos:

100.0% (87.58% / 95.27% / 18.01%)
Accuracy: 87.58% / 95.27% / 18.01%


## Ejercicio 4

### Resultados



#### General

| N \ Clasifier | LogisticRegression | MultinomialNB | LinearSVC |
|---|--------|--------|--------|
| 1 | 90.57% | 77.88% | 92.11% |
| 2 | 90.84% | 62.08% | 93.35% |
| 3 | 91.20% | 51.19% | 94.23% |
| 4 | 91.16% | 70.25% | 93.70% |

#### Known Words

| N \ Clasifier | LogisticRegression | MultinomialNB | LinearSVC |
|---|--------|--------|--------|
| 1 | 94.37% | 81.14% | 97.06% |
| 2 | 94.37% | 64.72% | 97.17% |
| 3 | 94.32% | 53.39% | 97.46% |
| 4 | 94.53% | 73.07% | 97.26% |


#### Unknown Words

| N \ Clasifier | LogisticRegression | MultinomialNB | LinearSVC |
|---|--------|--------|--------|
| 1 | 56.14% | 48.39% | 47.29% |
| 2 | 58.84% | 38.21% | 58.76% |
| 3 | 62.97% | 31.20% | 64.99% |
| 4 | 60.62% | 44.72% | 61.53% |