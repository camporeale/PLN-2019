Trabajo Práctico 2 - Análisis de Sentimiento
==============================================


Ejercicio 1 - Corpus de Tweets: Estadísticas Básicas
-------------------------------------------------------

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



Ejercicio 2 - Mejoras al Clasificador Básico de Polaridad
---------------------------------------------------------

Al empezar a hacer las pruebas notamos que la cantidad de ejecuciones necesarias y datos a comparar era muy grande, por lo que decidimos guardar los datos que produce el script eval.py dentro de un csv para poder levantarlo luego como un dataframe y lograr hacer una análisis más sencillo.

Modificamos eval.py para almacenar los datos en el csv, y la clase Evaluator para agregar la función get_results() que devuelve una lista con todos los valores reportados.

Para las pruebas seleccionamos las siguientes mejoras:

1. NLTK Tokenizer
2. Binarización de conteos
3. Normalización de tweets
4. Filtrado de stopwords

En la siguiente imagen pueden verse los resultados de cada una de las pruebas:

https://github.com/camporeale/PLN-2019/blob/master/sentiment/results.png

En líneas generales podemos decir que la mayoría de los cambios aportan similares mejoras en accuracy, siendo el uso de NLTK Tokenizer el que aportó la mayor ganancia (55.73 acc para corpus ES). La combinación de los 4 cambios produjo resultados ligeramente inferiores a este.



Ejercicio 3 - Exploración de Parámetros ("Grid Search")
-------------------------------------------------------


Ejercicio 4 - Inspección de Modelos
-----------------------------------

N:
  + poco sola cosa pobre mismo odio ni feo peor triste
  - bonito buen guapa encuentre 11:11 irresponsable buena genial algunos voy 

NEU:
  + pelado slammactivao encuentre 11:11 imdariusb1tches ineternete crtkftauryn plan nerviosa viejas
  - gracias su peor hoy triste ana feo sola ? cosas


NONE:
  + fecha ichuso empezado indirecta abstracto caspitoo semana distraído yaaa clrealy
  - mal buen ser nada serio feliz están más siempre sin
  
P:
  + buenos mejor enfadada genial feliz irresponsable cariñoso bonito buen guapa
  - triste ni plan largo horas alguien echo o mundo pobre


En líneas generales, los pesos de los features tienen sentido respecto a las clases, palabras con carga semántica positiva aparecen con gran peso favorable en la clase, y lo mismo para las negativas en la clase N. En NEU y NONE vemos que features de gran peso en N o P aparecen como fuertemente negativas.

También podemos notar que NEU y NONE incluyen en sus features más positivas palabras claramente mal escritas (ineternete) o nombres de usuarios (ichuso, caspitoo, etc). Podrían preprocesarse los tweets para eliminar los nombres de usuario como se hizo en el ejercicio 2, o usar diccionarios para eliminar palabras o realizar autocorrección antes de clasificar.



Ejercicio 5 - Análisis de Error
-----------------------------------

