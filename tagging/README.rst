==============================================
Trabajo Práctico 2 - Etiquetado de Secuencias
==============================================


Ejercicio 1 - Corpus AnCora: Estadísticas de etiquetas POS
----------------------------------------------------------

.. image:: https://github.com/camporeale/PLN-2019/blob/master/tagging/images/ancora_stats.png
   :width: 35pt

========  ==================
 Tag      Meaning
========  ==================
sp000     Preposición
nc0s000   Sustantivo Singular
da0000    Artículo
aq0000    Adjetivo Descriptivo
fc        Coma
np00000   Sustantivo - Nombre Propio
nc0p000   Sustantivo - Común Plural
fp        Punto
rg        Adverbio
cc        Conjunción
========  ==================


Ejercicio 2 - Baseline Tagger
----------------------------------------------------------

Se implementó la clase BaselineTagger que etiqueta cada palabra en base a su etiqueta más frecuente.


Ejercicio 3: Entrenamiento y Evaluación de Taggers
----------------------------------------------------------

El BaselineTagger produjo los siguientes resultados:

- Accuracy: 87.58% (82991/94758)
- Known words accuracy: 95.27% (81294/85333)
- Unknown words accuracy: 18.01% (1697/9425)

.. image:: https://github.com/camporeale/PLN-2019/blob/master/tagging/images/baseline_tagger_conf_matrix.png
   :width: 35pt


Ejercicio 4: Hidden Markov Models y Algoritmo de Viterbi
----------------------------------------------------------

- Se implementó la clase MLHMM
- Se implementó la clase ViterbiTagger


Ejercicio 5: HMM POS Tagger
----------------------------------------------------------

- N = 1
    - Accuracy (total/known/unknown): 63.50% / 70.50% / 0.15%
    - Time (real/user/sys): 2m24,786s / 2m24,691s / 0m0,173s


- N = 2
    - Accuracy (total/known/unknown): 91.34% / 97.63% / 34.33%
    - Time (real/user/sys): 2m23,061s / 2m22,820s / 0m0,209s


- N = 3
    - Accuracy (total/known/unknown): 91.87% / 97.65% / 39.50%
    - Time (real/user/sys): 4m9,960s / 4m9,035s /	0m0,296s

- N = 4
    - Accuracy (total/known/unknown): 91.61% / 97.31% / 40.01%
    - Time (real/user/sys): 19m12,318s / 19m0,915s / 0m5,356s


Ejercicio 6: Three words classifier
----------------------------------------------------------

Para este ejercicio creamos un script de entrenamiento train_classifier.py, será utilizado en el ejercicio 7 también

- Logistic Regression:
    - Accuracy (total/known/unknown): 91.69% / 95.01% / 61.68%
    - Time (real/user/sys): 0m4,890s / 0m4,885s / 0m0,217s

- SVM:
    - Accuracy (total/known/unknown): 94.11% / 97.57% / 62.76%
    - Time (real/user/sys): 0m5,242s / 0m5,159s / 0m0,249s

- Multinomial Naive Bayes:
    - Accuracy (total/known/unknown): 84.28% / 88.07% / 49.99%
    - Time (real/user/sys): 2m53,696s / 1m29,830s / 1m23,520s


Ejercicio 7: Clasificador con Word Embeddings fastText
----------------------------------------------------------
