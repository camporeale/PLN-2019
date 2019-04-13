Ejercicio 1: Corpus
===================

Para este ejercicio utilizamos el corpus de las traducciones de sesiones del parlamento europeo publicadas en:

	http://www.statmt.org/europarl/v7/es-en.tgz

De este corpus tomamos 200.000 sentencias para entrenamiento y 20.000 para evaluación, para descargarlos:

	https://github.com/camporeale/Datos/raw/master/eu_parlamento_corpus_part.zip
	https://github.com/camporeale/Datos/raw/master/euro_eval.zip

El PlaintextCorpusReader de ntlk funciona bastante bien para tokenización de este corpus:

	corpus = PlaintextCorpusReader('.', 'eu_parlamento_corpus.txt')
	corpus.sents()[0][0:20]

	['Los',
	 'socialdemócratas',
	 'daneses',
	 'votamos',
	 'a',
	 'favor',
	 'del',
	 'informe',
	 'del',
	 'Sr',
	 '.',
	 'Whitehead',
	 '.']

Ejercicio 2: Modelo de n-gramas
================================

En la clase NGram implementamos las siguientes funciones: 
	_init_: agregamos tokens especiales de inicio "<s>" y fin "</s>" a cada sentencia, creamos el diccionario con el conteo de n-gramas y n-1 gramas necesarios para poder realizar los cálculos de probabilidades
	count: retornamos el conteo correspondiente al n-grama o n-1 grama provisto
	cond_prob: calculamos la probabilidad de un ngrama en base a los counts tomados en _init_
	sent_prob: calculamos probabilidad de la sentencia multiplicando la probabilidad de todos los ngramas que encontramos en la misma  
	sent_prob_log: calculamos log probabilidad de la sentencia sumando log probabilidad de todos los ngramas

 
Ejercicio 3: Generación de Texto
================================
En la clase NGramGenerator implementamos:

	__init__: obtenemos todos los ngramas del modelo, calculamos sus probabilidades correspondientes y las almacenamos en un diccionario
	generate_token: dado tokens iniciales, seleccionamos un nuevo token al azar en base a las probabilidades almacenadas en el diccionario
	generate_sent: iteramos con generate_token comenzando con ngrama-1 caracteres de inicio "<s>", hasta que se genere un caracter de fin de sentencia "</s"


	Unigrama:
	"unívocamente olvidar en corremos importante mercancía valorar con su judicial hombre de que Es Unión"
	"enmiendas sanitarias de , la de comparables En Necesitamos de sobre paro a esta un . las común Roja De de enmiendas Unión , humanos que a líneas ningún que y"
	"de hoy que 9"
	"que posibilidades los lo puedo Sin en los este penas hace sobre sentido entre . de en"

	Bigramas:
	"Al igual que tener que este proceso de objetivo de fondo las solicitudes de que los productos no es decir Sound Economic Management )."
	"El PNB , si es una evaluación de carbono - al estudiarlas ."
	"Gracias , esas críticas a continuación las fuentes de toma de intervenir , de las dos veces no ?"
	"La cual equivale a la única no agrade a favor de conformidad con algunas veces ."

	Trigramas:
	"Si no hay legislación comunitaria consagró la posibilidad de hacerlo."
	"Señor Presidente , estimados , aunque los servicios postales o en Asia ha modificado los aspectos de esta Asamblea."
	"De acuerdo con la mayor brevedad , permítame en primer lugar , que luego no otra cosa."
	"No me apasiono con este principio del domingo 12 de mayo de 1998 , para nosotros son extraordinariamente escasos."


	Cuatrigramas:
	"Cabe partir del principio de justicia universal y , entre otras , las enmiendas 10 , 15 y la 16 -, que nos parecen esenciales : la vigilancia multilateral , las grandes potencias , incluidas las organizaciones no gubernamentales que hubiera tenido que merecer un tratamiento por separado."
	"En relación con estas tendencias futuras."
	"Por eso , los hijos son un bien público , tienen que aprobarse todas las enmiendas presentadas por la Sra."
	"Con la ayuda de cooperación en el ámbito audiovisual."


Ejercicio 4: Suavizado "add-one"
================================

En la clase AddOneNGram, implementamos:
	__init__: Su única modificación respecto a NGram es que calculamos el tamaño total del vocabulario para poder realizar el cálculo de addone
	V: devuelve el tamaño del vocabulario	
	cond_prob: calculamos probabilidad de ngrama sumando 1 al conteo del ngrama y el vocabulary size al conteo de prev_tokens
	
El resto de las funciones se heredan de NGram


Ejercicio 5: Evaluación de Modelos de Lenguaje
==============================================

Usando la siguiente documentación: https://wiki.cs.famaf.unc.edu.ar/lib/exe/fetch.php?media=materias:pln:2019:lm-notas.pdf, implementamos sobre la clase LanguageModel:
	
	log_prob: calculamos la log probabilidad del conjunto completo de sentencias (suma de log probabilidad de cada sentencia)
	cross_entropy: calculamos crossentropy (inverso de log probabilidad de las sentencias dividido el total de palabras del corpus)
	perplexity: calculamos perplexity (2 elevado al valor de crossentropy), retornamos perplexity, crossentropy, log_prob

El resultado de la evaluación de los modelos addone fue el siguiente:

	Unigrama:
	Log probability: -5911036.68
	Cross entropy: 9.90
	Perplexity: 955.43

	Bigrama:
	Log probability: -6088296.78
	Cross entropy: 10.20
	Perplexity: 1173.73

	Trigrama:
	Log probability: -7934079.71
	Cross entropy: 13.29
	Perplexity: 10003.86

	Cuatrigrama:
	Log probability: -8881233.76
	Cross entropy: 14.87
	Perplexity: 30039.95


Ejercicio 6: Suavizado por Interpolación
=========================================

En proceso

