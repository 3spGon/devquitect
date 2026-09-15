# Verificación de entregas por slice

Status: Approved
Last updated: 2026-09-14

## Confirmed

El usuario solicita analizar y optimizar su protocolo de verificación con Devquitect,
contrastarlo con OpenSpec y conservar el trabajo en una nueva sesión `slice-verification`.
Confirma que siempre debe verificarse al terminar de trabajar un slice. Esta solicitud
autoriza definición persistente; todavía no autoriza modificar las skills ni implementar.

El contrato actual de [ejecución](../../../skills/project-plan-execution/references/execution.md)
ya exige evaluar los criterios, ejecutar checks y registrar evidencia antes de marcar
`verified`. El contrato de [estado de entrega](../../../skills/project-plan-execution/references/delivery-state.md)
ubica el checkpoint en la misma sesión de diseño y distingue `implemented` de `verified`.
La propuesta concreta cómo demostrar cada criterio, pero duplica evidencia entre dos archivos.

## Assumptions

- Se conserva la carpeta por iniciativa y el checkpoint existente, según Gate 1 aprobado.
- El primer alcance es la entrega desde planes persistentes aprobados. No se obliga a una
  tarea ad hoc a crear un plan y un tracker ficticios para poder verificarla.
- Los reportes Markdown facilitan auditoría y continuidad, pero no prueban por sí mismos
  que una ejecución ocurrió o que la prueba representa correctamente el requisito.

## Open decisions

Gate 1 aprobado explícitamente por el usuario el 2026-09-14. No quedan decisiones de producto abiertas.
No se propone adoptar OpenSpec como dependencia ni migrar sesiones existentes.

## Objetivo y límites

El resultado buscado es que el agente cierre cada slice con evidencia vigente de todos sus
criterios requeridos, corrija fallos recuperables y permita a una persona entender qué se
comprobó y sobre qué estado. Los actores son quien autoriza la entrega, el agente que la
ejecuta y quien revisa sus resultados.

La secuencia propuesta es: identificar criterios → implementar → verificar el slice →
corregir y volver a verificar si falla → registrar evidencia → marcar `verified` → continuar
con el siguiente slice autorizado. La revisión acumulada al final de la entrega se conserva.

No se incluyen publicación, despliegue, cambios automáticos al plan aprobado, nuevos gates
humanos por slice, ejecución model-backed sin autorización ni un sistema general de CI.

## Dónde guardar la evidencia

Recomiendo mantener una unidad por iniciativa:

```text
docs/software-design/<session>/
  00-status.md                 # Estado de la definición
  02-requirements.md           # Criterios y comportamiento esperado
  08-implementation-plan.md    # Slices aprobados, cuando corresponda
  09-delivery-status.md        # Autoridad de entrega, resumen y enlaces
  slices/
    SLICE-001.md               # Detalle de verificación de ese slice
```

Este árbol describe la entrega futura, no archivos que deban crearse en esta sesión ahora.
`slices/` contiene evidencia subordinada al checkpoint, no otro plan ni otro motor de estado.
Los criterios conservan su autoridad en los requisitos y el plan; el checklist los referencia.

Aunque `software-design` no es un nombre perfecto para todo el ciclo, separar una raíz
`plan-execution/` no mejora por sí solo la verificación. Sí obliga a revisar descubrimiento,
rutas relativas, enlaces y compatibilidad. Solo reconsideraría esa separación si aparecen
ejecuciones independientes con permisos, retención o múltiples ciclos de entrega que la
estructura actual no pueda representar con claridad.

## Contraste con OpenSpec

Consulta de documentación oficial: 2026-09-14, rama `main`; referencia mutable.

| Aspecto | Devquitect actual y propuesta | OpenSpec |
| --- | --- | --- |
| Unidad de trabajo | Sesión con definición, plan y entrega enlazados | Carpeta de cambio con propuesta, diseño, tareas y deltas |
| Comportamiento vigente | System Context orienta y enlaza fuentes detalladas; no es una especificación exhaustiva | `specs/` contiene especificaciones vigentes; `changes/` separa modificaciones propuestas |
| Avance | Gates explícitos y autorización concreta de slices | Flujo flexible guiado por artefactos |
| Verificación | Se propone evidencia por criterio y bloqueo de cierre ante pendientes | `verify` evalúa completitud, corrección y coherencia |

La organización y el flujo de OpenSpec están descritos en sus
[conceptos](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md).
Su [comando verify](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md)
busca evidencia en el código y reporta problemas; la documentación aclara que ese reporte
no bloquea por sí mismo el archivo. El CLI además ofrece
[validación estructural y comprobación de tareas archivadas](https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md).
Ni una casilla marcada ni una validación de estructura equivalen a ejecutar el comportamiento.

Mi inferencia: conviene tomar de OpenSpec la distinción entre comportamiento esperado,
cambio y tareas, y la comprobación de completitud/corrección/coherencia. No hace falta
copiar su estructura ni mantener dos fuentes canónicas en paralelo. Una futura especificación
consolidada por capacidad sería otra iniciativa, si las sesiones históricas dificultan conocer
el comportamiento vigente.

## Opinión: funcionará con estas condiciones

Sí recomiendo verificar siempre antes de cerrar cada slice. Reduce la distancia entre
introducir un fallo y descubrirlo, evita propagar dependencias sin demostrar y deja un punto
fiable para retomar trabajo. Es una valoración de diseño, no un resultado experimental.

La obligación debe ser verificar todos los criterios aplicables, no ejecutar todas las
herramientas disponibles. Un slice de documentación no necesita navegador; uno que cambia
foco o submit sí necesita evidencia de la aplicación ejecutada. Los checks obligatorios del
repositorio siempre se respetan aunque la selección del slice sea más estrecha.

El enfoque fallaría si el checklist se convierte en tareas genéricas, si se rellenan `PASS`
de antemano, si un test indirecto sustituye un criterio, si se conserva evidencia obsoleta o
si dos tablas discrepan. También fallaría como garantía absoluta: una instrucción al modelo
no puede asegurar que sus propias afirmaciones sean verdaderas.

Por eso propongo un control determinista de consistencia antes de aceptar el cierre,
limitado a lo comprobable: cobertura de criterios, estados, referencias y resultados
requeridos. Su diseño técnico queda para después de Gate 1. Ese control no certificará
semánticamente una captura, un resultado manual ni la calidad de una prueba.

## Perfil y experiencia

Cambio de comportamiento y cambio técnico, impacto acotado, profundidad estándar.
Afecta ejecución, calidad y la lectura de resultados. No requiere migrar checkpoints ni
cambiar autorizaciones; el detalle del control de cierre debe definirse antes de Gate 2.
Se preservan las sesiones existentes y la distinción entre definición, entrega y revisión.

La interacción es mínima: consultar el resultado de un slice, distinguir fallo de ausencia
de evidencia, localizar un bloqueo y retomar. Sus estados y recuperación se definen en
[02-requirements.md](02-requirements.md); no se necesita interfaz gráfica ni otro artefacto UX.
La reversión de una futura adopción deberá conservar la evidencia y las rutas existentes.
