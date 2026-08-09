# Datos personales

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/personal-data.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/personal-data.md">简体中文</a> ·
  <strong>Español</strong> ·
  <a href="../../../pt-BR/docs/architecture/personal-data.md">Português (BR)</a> ·
  <a href="../../../vi/docs/architecture/personal-data.md">Tiếng Việt</a> ·
  <a href="../../../en-x-aibro/docs/architecture/personal-data.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

## La frontera

El plugin es código público. El espacio de trabajo es el historial laboral, las
cifras de compensación y las restricciones de una persona. Son cosas distintas y
viven en directorios distintos, y casi toda regla de esta página se sigue de esa
sola frase.

`/slushpile:onboard` se corre en tu propio directorio, no en el checkout del
plugin. Ahí escribe `profile.md`, `preferences.yaml` y `stories.md`. El
onboarding dice claramente que ese directorio debería ser un repositorio
**privado** o ningún repositorio, y no va a inicializar uno ni agregar un
remoto: esa es una decisión que se toma deliberadamente, no un efecto colateral
de montar un espacio de trabajo.

## Nada en `skills/` ni en `agents/` puede fijar un dato sobre ningún usuario

Nada de pisos de compensación. Nada de tablas de renta por ciudad. Nada de
ciudadanía, nada de estado de habilitación de seguridad, ningún empleador con
nombre presentado como propio del usuario, ninguna historia con nombre, ningún
"el candidato está abierto a mudarse". Una habilidad que necesite algo de eso lo
lee de `preferences.yaml` en tiempo de ejecución.

La falla que esto previene es específica y silenciosa. Un piso de compensación
fijo no da error; mata puestos, con apariencia de corrección, por una razón que
tú nunca elegiste y no puedes ver. Un "abierto a mudarse" fijo tampoco da error;
produce doce postulaciones que afirman algo sobre alguien que podría no ser
cierto.

Los ejemplos ilustrativos que nombran empresas reales están bien, y son útiles,
porque enseñan el patrón. *"La mayoría de los candidatos a planificación de
capacidad vienen de un solo lado"* como ejemplo de una tesis que depende de la
empresa es enseñanza. *"El candidato tiene diez años en sistemas de control
industrial"* es una fuga.

Nota que el segundo ejemplo tuvo que parafrasearse para poder aparecer en esta
página. El real nombra un dominio que `check_no_pii.py` detecta, y este archivo
es uno de los archivos que escanea, que es la barrera funcionando como se
pretendía, sobre la página que la documenta.

## La barrera

```bash
python3 scripts/check_no_pii.py
```

Escanea `skills/`, `agents/`, `templates/` y `docs/` buscando los patrones que
se filtraron la última vez, cada uno con la razón por la que cuenta como fuga:
identidad del autor, un empleador previo declarado como propio del usuario, una
ubicación de residencia fija, una línea base de compensación fija, un estado de
ciudadanía o de habilitación de seguridad declarado como hecho, una credencial
declarada como hecho, datos de contacto reales, y referencias a archivos que
existen solamente en el repositorio privado del que se productizó este plugin.

Los patrones son deliberadamente angostos. Un patrón amplio que se dispara sobre
prosa legítima queda suprimido en una semana, y un chequeo suprimido es peor que
ningún chequeo porque se lee como cobertura.

Un patrón de fuga nuevo que se cuele pertenece a ese script, no a un comentario
de revisión.

## La única exención, y su límite

Los agentes de voz están exentos de los patrones de **identidad**, y solo de
esos. Un agente de voz *es* la identidad de una persona por construcción: se
genera a partir de un corpus de su escritura, lleva su nombre, y sus ejemplos
son sus oraciones reales. Quitarle la identidad destruiría el artefacto.

Los datos de contacto están prohibidos en todas partes, agentes de voz
incluidos. Un número de teléfono en un agente distribuido es una fuga bajo
cualquier teoría.

La lista de exenciones es por archivo y por patrón, en
`check_no_pii.VOICE_AGENTS`. Hay una segunda lista, `ALLOWED`, para todo lo
demás, y está vacía a propósito. Cada entrada sería un agujero, y un agujero en
esta barrera es invisible hasta que la postulación de otra persona dice que está
abierta a mudarse a una ciudad que nunca vio.

## El pipeline nunca envía nada

Ninguna habilidad toca un portal de postulaciones, un correo ni un formulario.
Cada etapa escribe archivos. Tú los lees y los envías.

Esto es una propiedad de privacidad antes que de seguridad: un pipeline que
envía es un pipeline que tiene que guardar credenciales, y en este diseño no hay
ningún lugar donde ponerlas que no sea tu propia máquina haciendo algo que no
supervisaste.
