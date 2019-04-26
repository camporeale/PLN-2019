==============================================
Trabajo Práctico 2 - Análisis de Sentimiento
==============================================

El código utilizado en los ejercicios se encuentra en el siguiente notebook:

https://github.com/camporeale/PLN-2019/blob/master/sentiment/Ejercicios%20Practico%202.ipynb


Ejercicio 1 - Corpus de Tweets: Estadísticas Básicas
====================================================

Creamos el script stats.py, el mismo produce el siguiente output en el conjunto 

python stats.py -c ./sentiment/InterTASS

Corpus ES
  Length: 1008
  Polarity:  {'NONE': 139, 'N': 418, 'P': 318, 'NEU': 133}

Corpus CR
  Length: 800
  Polarity:  {'NONE': 165, 'NEU': 94, 'N': 311, 'P': 230}

Corpus PE
  Length: 1000
  Polarity:  {'P': 231, 'NEU': 166, 'N': 242, 'NONE': 361}



Ejercicio 2 - Mejoras al Clasificador Básico de Polaridad
---------------------------------------------------------

Al empezar a hacer las pruebas notamos que la cantidad de ejecuciones necesarias y datos a comparar era muy grande, por lo que decidimos guardar los datos que produce el script eval.py dentro de un csv para poder levantarlo luego como un dataframe y lograr hacer una análisis más sencillo.

Modificamos eval.py para almacenar los datos en el csv, y la clase Evaluator para agregar la función get_results() que devuelve una lista con todos los valores reportados.

Para las pruebas seleccionamos las siguientes mejoras:

1. NLTK Tokenizer 
2. Binarización de conteos
3. Filtrado de stopwords
4. Normalización de tweets

- Los tres primeros se implementaron como opciones del vectorizador en la función init de SentimentClassifier:

        CountVectorizer(tokenizer=word_tokenize,binary=True,stop_words=list(stopwords.words('spanish')))

- La normalización de tweets creando la función normalize() en la misma clase y llamandola desde eval.py y train.py antes de fit() y predict() respectivamente 

En la siguiente imagen pueden verse los resultados de cada una de las pruebas:

.. image:: https://github.com/camporeale/PLN-2019/blob/master/sentiment/results.png
   :width: 40pt
    

En líneas generales podemos decir que la mayoría de los cambios aportan similares mejoras en accuracy, siendo el uso de NLTK Tokenizer el que aportó la mayor ganancia (55.73 acc para corpus ES). La combinación de los 4 cambios produjo resultados ligeramente inferiores a este.



Ejercicio 3 - Exploración de Parámetros ("Grid Search")
-------------------------------------------------------

Los mejores resultados obtenidos fueron:

- Logistic Regression:  C=0.1, penalty=l2
- SVM:                  C=0.01, penalty=l2
- NultinomialNB:        alpha=1



Ejercicio 4 - Inspección de Modelos
-----------------------------------

N:

- Coeficientes mas altos: 
      poco sola cosa pobre mismo odio ni feo peor triste
- Coeficientes más bajos:
      bonito buen guapa encuentre 11:11 irresponsable buena genial algunos voy

NEU:

- Coeficientes mas altos:
      pelado slammactivao encuentre 11:11 imdariusb1tches ineternete crtkftauryn plan nerviosa viejas
- Coeficientes mas bajos:
      gracias su peor hoy triste ana feo sola ? cosas


NONE:

- Coeficientes mas altos:
      fecha ichuso empezado indirecta abstracto caspitoo semana distraído yaaa clrealy
- Coeficientes más bajos:
      mal buen ser nada serio feliz están más siempre sin
  
P:

- Coeficientes mas altos:
      buenos mejor enfadada genial feliz irresponsable cariñoso bonito buen guapa
- Coeficientes mas bajos:
      triste ni plan largo horas alguien echo o mundo pobre


En líneas generales, los pesos de los features tienen sentido respecto a las clases, palabras con carga semántica positiva aparecen con gran peso favorable en la clase, y lo mismo para las negativas en la clase N. En NEU y NONE vemos que features de gran peso en N o P aparecen como fuertemente negativas.

También podemos notar que NEU y NONE incluyen en sus features más positivas palabras claramente mal escritas (ineternete) o nombres de usuarios (ichuso, caspitoo, etc). Podrían preprocesarse los tweets para eliminar los nombres de usuario como se hizo en el ejercicio 2, o usar diccionarios para eliminar palabras o realizar autocorrección antes de clasificar.



Ejercicio 5 - Análisis de Error
-----------------------------------

Tomamos como ejemplo el siguiente tweet:

- "@LaQueSoySiempre @ealbaga Por desgracia vende más  ,riñas,trifulcas,peleas,al cuello!! mátalo!!"

Esta instancia tuvo una predicción de clase "P" con una probabilidad de 0.991105, siendo su clase verdadera "N". Los coeficientes de los features eran los siguientes:

- "!" [-1.00453974 -0.95153362 -0.19846824  1.36069119]

- "," [-0.3870915  -0.07526614 -0.39497008  0.50956257]

- "@" [-0.37599216 -0.21543827  0.2713075   0.06814566]

- "al" [ 0.51110109 -0.39551092  0.05058118 -0.4960745 ]

- "desgracia" [ 0.61744223 -0.21158639 -0.09616715 -0.21244867]

- "más" [-0.52540095  1.27775123 -1.20268792  0.18649803]

- "por" [-0.54276769  0.50699498 -0.44647751  0.31744384]

- "vende" [ 0.38222646 -0.44397838  0.48114509 -0.38853147]

Los que tenían mayor peso en la clasificación como P de la instancia eran "!" y ",". Probamos sacando primero una y luego la otra, pero se mantuvo igual. Cuando removimos ambas, la clasificación cambio a N. El signo de exclamación quizás puede interpretarse como alegría o sorpresa, pero su peso parece desproporcionado. 

Intentemos entrenar una regresión logística eliminando tanto comas como signos de exclamación, pero los resultados fueron ligeramente peores ¿Quizás los tweets con sentimientos positivos suelen hacer uso más común del signo de interrogación?


Ejercicio 6 - Evaluación Final
-----------------------------------

Modificamos eval.py para leer el archivo con los resultados del corpus de Test cuando use la opción "-f":

.. code-block:: python

    corpus = opts['-c']
    if opts['--final']:
      reader = InterTASSReader(corpus,res_filename="InterTASS/ES/TASS2017_T1_test_res.qrel")
    else:
      reader = InterTASSReader(corpus)
    corpus = opts['-c']
    if opts['--final']:
      reader = InterTASSReader(corpus,res_filename="InterTASS/ES/TASS2017_T1_test_res.qrel")
    else:
      reader = InterTASSReader(corpus)

Y luego entrenamos un modelo SVM y lo evaluamos con el corpus de Test:

python scripts/eval.py -i svm_nltk_es -c "InterTASS/ES/intertass-ES-test.xml" -f -d "TEST SET - SVM with nltk tokenize"

El resultado fue el siguiente: 

.. image:: https://github.com/camporeale/PLN-2019/blob/master/sentiment/test_corpus_results.png
   :width: 40pt