Trabajo Práctico 2 - Análisis de Sentimiento
==============================================


Ejercicio 1
-----------

Creamos el script stats.py, el mismo produce el siguiente output en el conjunto 

python stats.py -c ./sentiment/InterTASS
Corpus ES
  Length: 1008
   Polarity: 
       NONE 139
       N 418
       P 318
       NEU 133
Corpus CR
  Length: 800
   Polarity: 
       NONE 165
       NEU 94
       N 311
       P 230
Corpus PE
  Length: 1000
   Polarity: 
       P 231
       NEU 166
       N 242
       NONE 361



Ejercicio 2
-----------

Al empezar a hacer las pruebas notamos que la cantidad de ejecuciones necesarias y datos a comparar era muy grande, por lo que decidimos guardar los datos que produce el script eval.py dentro de un csv para poder levantarlo luego como un dataframe y lograr hacer una análisis más sencillo.

Modificamos eval.py para almacenar los datos en el csv, y la clase Evaluator para agregar la función get_results() que devuelve una lista con todos los valores reportados.

Para las pruebas seleccionamos las siguientes mejoras:

1. NLTK Tokenizer
2. Binarización de conteos
3. Normalización de tweets
4. Filtrado de stopwords

En la siguiente imagen pueden verse los resultados de cada una de las pruebas:

https://github.com/camporeale/PLN-2019/blob/master/sentiment/results.png

En líneas generales podemos decir que la mayoría de los cambios aportan similares mejoras en accuracy, siendo el uso de NLTK Tokenizer el que aportó la mayor ganancia (55.73 acc para corpus ES)

La combinación de los 4 cambios produjo resultados ligeramente inferiores a este.


