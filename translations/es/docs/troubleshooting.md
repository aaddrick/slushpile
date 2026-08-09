# Solución de problemas

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/troubleshooting.md">English</a> ·
  <a href="../../zh-CN/docs/troubleshooting.md">简体中文</a> ·
  <strong>Español</strong> ·
  <a href="../../pt-BR/docs/troubleshooting.md">Português (BR)</a> ·
  <a href="../../vi/docs/troubleshooting.md">Tiếng Việt</a>
</p>

<!-- END GENERATED language-nav -->

**`plugin install` funciona pero las habilidades no aparecen.** Ejecuta `claude plugin
list` y busca `enabled`. Las habilidades se cargan al inicio de la sesión, así
que abre una sesión nueva o ejecuta `/clear`.

**Una habilidad dice que no encuentra `preferences.yaml`.** Estás en un
directorio distinto de aquel donde hiciste el onboarding. Cada habilidad lee el
espacio de trabajo desde el directorio de trabajo actual. Consulta
[El espacio de trabajo](workspace.md).

**Los agentes de la revisión reportan un currículum casi vacío.** Están leyendo
texto extraído, no tu PDF tal como se ve. Ejecuta `pdftotext yourresume.pdf -` y
mira la salida. Si está vacía o revuelta, el currículum tiene un problema de
maquetación (una grilla de varias columnas, un cuadro de texto, los datos de
contacto en un encabezado) y eso es un hallazgo real, no una falla de las
herramientas. Un ATS ve lo que ve `pdftotext`.

**La carta de presentación se lee genérica, o suena a otra persona.** Revisa
`voice.is_mine` en `preferences.yaml`. Si es falso estás usando la voz de
ejemplo que viene incluida, que es la del autor del plugin. Genera la tuya con
[written-voice-replication](https://github.com/aaddrick/written-voice-replication)
y apunta `voice.agent` hacia ella. Si ya es verdadero, lo más probable es que el
corpus haya quedado demasiado delgado: unos pocos miles de palabras son el piso.
Consulta [Tu agente de voz](voice.md).

**Todos los puestos vuelven descartados por compensación.** Abre
`preferences.yaml` y revisa `compensation`. Con `net_qol`, la causa más común es
un `current_baseline` cargado como monto bruto en lugar de neto después de
impuestos y de vivienda, lo que hace que toda oferta se vea peor de lo que es.

**Todos los puestos vuelven en Nivel 1.** Algo está calificando contra la
publicación en vez de contra el pool de postulantes. Verifica que
`role_analysis.md` de verdad contenga arquetipos por percentil para el puesto, y
no solo una comparación de palabras clave: un puntaje de ajuste sin una
estimación del pool detrás es un puntaje de coincidencia disfrazado de
percentil. Consulta
[Puntuación](architecture/scoring.md).

**La revisión nunca dice que no.** Verifica que el contrarian haya corrido
siquiera: su veredicto neto debería aparecer en el resumen del pipeline y en
`application.yaml` bajo `contrarian_net`. Se supone que es automático y no
condicional, y una revisión a la que le falta es una revisión sin paso de
falsación.

**La calibración dice que no hay datos suficientes, y claramente los hay.** El
piso son cinco postulaciones *resueltas*, y una postulación cuenta como resuelta
solo cuando `outcome.stage_reached` está definido, o cuando se envió hace más de
30 días sin respuesta. Las postulaciones que siguen en `application.yaml` con un
resultado vacío se cuentan como en curso, no como rechazos. `/slushpile:status`
informa qué registros están incompletos.

**Una ronda de revisión produce los mismos hallazgos que la anterior.** Eso es
la señal, no un error. Un problema marcado en más de una ronda es real; un
problema marcado una sola vez es ruido. Si para la tercera ronda nada se movió,
los huecos son estructurales, y se supone que el pipeline lo diga en lugar de
correr una cuarta ronda.

**El pipeline no va a enviar la postulación por ti.** Nunca lo va a hacer.
Ninguna habilidad toca un portal, un correo ni un formulario. Escribe archivos;
tú los lees y tú los envías.
