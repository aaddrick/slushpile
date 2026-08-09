# Puntuación

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/scoring.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/scoring.md">简体中文</a> ·
  <strong>Español</strong> ·
  <a href="../../../pt-BR/docs/architecture/scoring.md">Português (BR)</a> ·
  <a href="../../../vi/docs/architecture/scoring.md">Tiếng Việt</a>
</p>

<!-- END GENERATED language-nav -->

Cada número que produce este pipeline es la respuesta a una de dos preguntas:
dónde se ubica el candidato en la fila para este puesto específico, y cuánto
vale realmente una postulación por un canal dado. Nada de lo que hay aquí
puntúa un documento contra una publicación en aislamiento, porque ese es un
número real sobre la pregunta equivocada.

## Anclaje al pool

Un puntaje de coincidencia de palabras clave compara un currículum con una
descripción de puesto. A nadie lo contrata una descripción de puesto. La
comparación que decide el resultado es contra los demás postulantes de la fila,
y un puntaje de coincidencia no puede verlos.

Así que la etapa de búsqueda estima primero el pool de postulantes: quién más
se postula a esta vacante, y cómo son los postulantes de la mediana, del
percentil 75 y del percentil 90. Después se ubica al candidato en esa
distribución, y **el percentil dentro del pool se registra como el número
canónico de ajuste.** La coincidencia de palabras clave, si acaso se quiere, va
en un campo aparte. Colapsar los dos es exactamente la falla que la rúbrica
existe para prevenir.

| Posición en el pool | Nivel | Significado |
| --- | --- | --- |
| p75+ | Nivel 1 | Por encima de la vara del postulante fuerte para este puesto específico |
| p55–p74 | Nivel 2 | Competitivo, no diferenciado. Necesita una ventaja de canal. |
| p35–p54 | Nivel 3 | Debajo de la mediana. Persíguelo solo por un canal fuerte. |
| debajo de p35 | Descarte | El pool supera al candidato. Un envío en frío es un espacio desperdiciado. |

Las entradas están ordenadas. Dos o más calificaciones mínimas críticas sin
cumplir bajan la posición uno o dos niveles sin importar todo lo demás. Después
la comparación con el pool: ¿la afirmación más fuerte realmente destaca aquí, o
es mediana? Después la divergencia respecto al ritmo operativo real del
puesto, después los factores de riesgo a razón de aproximadamente cinco a diez
puntos percentiles cada uno, y después el prior de calibración para la empresa.

La salida más útil de esta etapa es un supuesto diferenciador que vuelve marcado
como mediano del pool. Esa es información que el candidato no puede obtener
de un escáner de documentos, y suele ser lo que cambia lo que escribe.

## Veredictos condicionados por canal

Los mismos materiales convierten a tasas muy distintas según cómo llegan. Un
veredicto único promedia esa diferencia y reporta el promedio como si fuera un
hecho sobre la postulación.

Por eso, todo puesto de Nivel 1 a 3 recibe una matriz en lugar de un veredicto:

| Canal | Condición | Rango aproximado de pasar el filtro |
| --- | --- | --- |
| Envío en frío | ninguna | 5–15%, varía con la posición en el pool |
| Referido tibio | tiene que existir alguien que refiera | 25–50%, depende del pool |
| Contacto en frío a un empleado con nombre | un objetivo identificable | 5–15% |
| Entrante desde trabajo público | un artefacto existente, ya sembrado | 20–40% si prende |
| Entrante de un reclutador | fuera del control del candidato | no se estima |

Dos reglas evitan que esto sea decorativo.

**El nivel del puesto es el nivel más alto entre los canales *disponibles***, y
la matriz registra qué canal lo desbloquea y qué condición hay que cumplir. Si
hoy no existe nadie que refiera, la fila del referido tibio es solo informativa
y no desbloquea el Nivel 1. Inflar un nivel apoyándose en un canal
no disponible es la forma más común de hacer trampa con esta matriz, y es
autoinfligida.

**Tu propio historial le gana a cualquier prior.** Cuando `job_search.md`
registra una tasa real de referido tibio en esta empresa, se usa ese número
en lugar del genérico. Ve
[memory-and-calibration.md](memory-and-calibration.md).

## La calidad de los materiales no es el valor esperado

La revisión los reporta como dos números separados porque suelen no coincidir.
Materiales excelentes enviados a un puesto mal ajustado igual tienen valor
esperado bajo; materiales adecuados enviados por un referido a un puesto bien
ajustado tienen valor esperado alto.

Colapsarlos te dice que gastes otra hora editando cuando la recomendación
honesta es gastar esa hora consiguiendo a alguien que te refiera. Un puntaje de
materiales de 8/10 junto a una conversión en frío de 1–3% no es una
contradicción: es el hallazgo completo.

## Criterios de descarte

Los criterios de descarte corren al momento del escaneo y se contrastan contra
`preferences.yaml`: compensación, ubicación, habilitación de seguridad y
cualquier otra cosa que hayas registrado como restricción.

Dos propiedades importan más que la lista misma.

**Los que pasan se declaran, no solo los que fallan.** Un chequeo que reporta
únicamente lo que falló es indistinguible de un chequeo que no corrió, y aquí no
hay intérprete que pruebe que corrió.

**Un descarte nombra su único bloqueador principal.** Si ningún bloqueador
justifica por sí solo descartar el puesto, el puesto recibe un puntaje en lugar
de un descarte. Un descarte justificado por la acumulación de dudas pequeñas es
un estado de ánimo, y no va a sobrevivir a que tú mismo lo releas una semana
después.

La compensación se evalúa sobre la **banda publicada**, usando el método
registrado en `preferences.yaml`. Los términos de la etapa de oferta están
explícitamente fuera de alcance aquí por la misma razón por la que se eliminan
en la revisión: ve [the-review.md](the-review.md#the-gatekeeper).

## Rangos de probabilidad, no palabras de veredicto

La salida es "1–3% de entrevista" en lugar de "QUIZÁ". Un rango carga su propia
incertidumbre y se puede contrastar contra lo que realmente pasó; una palabra de
veredicto no carga ninguna de las dos cosas y no se puede contrastar.

Esto también es lo que hace posible el ciclo de calibración. "QUIZÁ" no se puede
regresar contra los resultados. Un porcentaje sí, y
[memory-and-calibration.md](memory-and-calibration.md) es donde ocurre esa
regresión.
