# suicide-news-classifer-spanish


[![PyPI version](https://badge.fury.io/py/domestic_violence_news_classifer_spanish.svg)](https://badge.fury.io/py/domestic_violence_news_classifer_spanish)

To install it

```
 pip install suicide-news-classifer-spanish
```

you will also need tensorflow and keras to run this package so

```
 pip install tensorflow keras
```

Import the package

```
from suicide_news_classifer_spanish import suicide_classifier

```

we will use the following text to test it:

```
text_new = "Una mujer de 39 años murió en las últimas horas en un hospital de Santa Fe luego de agonizar desde el 11 de marzo, cuando su hijo la roció con nafta y la prendió fuego, en la localidad de Bella Italia, lindante con Rafaela, informaron hoy fuentes policiales. Los voceros identificaron a la víctima como Romina Esther Leiva (39), en tanto el acusado del ataque es su hijo Miguel Ángel Beresvilj (25), quien está detenido a la espera del juicio. Leiva murió mientras era asistida en la sala de terapia intensiva del hospital José María Cullen de la capital santafesina, luego de sufrir graves quemaduras en el 80 por ciento de su cuerpo que le afectaron el rostro, tórax, brazos y la pierna izquierda. La mujer resultó quemada en el marco de un violento episodio en su casa, situada en calle Córdoba al 100, de Bella Italia, localidad ubicada unos 95 kilómetros al oeste de la ciudad de Santa Fe. Luego del ataque, Beresvilj escapó en su motocicleta y horas después fue atrapado por la policía en la localidad de Frontera, en el límite con la provincia de Córdoba. En el domicilio donde ocurrió la agresión la Policía de Investigaciones secuestró dos bidones de cinco litros con restos de nafta. La versión del muchacho ante la Justicia es que su intención era quemar el automóvil de la pareja de su madre, con quien mantenía una mala relación, y que su madre se interpuso y resultó quemada por accidente. La fiscal de la Unidad de Violencia de Género, Familiar y Sexual del Ministerio Público de la Acusación (MPA), Ángela Capitanio, imputó a Beresvilj por el delito de ?homicidio agravado por el vínculo y por mediar violencia de género, en grado de tentativa, aunque ahora cambiará de figura penal ante la muerte de la mujer. El acusado se encuentra detenido con prisión preventiva sin plazos por orden del juez Osvaldo Carlos. Voceros judiciales indicaron que en la audiencia donde se fijó la prisión preventiva, el acusado dijo que jamás tuvo la intención de lastimar a su madre y que solo quería arruinarle el auto a (Roberto) Mansilla, el esposo de Leiva. Romina Leiva tenía, además de Beresvilj, cuatro hijos, dos mellizos de 13 años y otros dos de 9, producto de una relación anterior."
```

run the classifier:

```
classifier = domestic_violence_classifier.DomesticViolenceClassifier()
print(classifier.domestic_violence_subject_probability(text_new))

```

you will see that it outputs 

```
0.9789301
```