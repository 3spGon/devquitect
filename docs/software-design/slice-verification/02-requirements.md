# Contrato propuesto de verificación

Status: Approved
Last updated: 2026-09-14

## Confirmed

Debe verificarse siempre al terminar el trabajo de cada slice. Se mantienen las autorizaciones
y criterios del plan aprobado, la corrección de fallos recuperables y la evidencia vigente.

## Assumptions

Se conserva un archivo de detalle por slice ejecutado y un resumen enlazado desde el tracker.
Gate 1 fue aprobado explícitamente por el usuario el 2026-09-14; no autoriza implementación.

## Open decisions

Ninguna decisión de producto pendiente. El tratamiento técnico se define después de Gate 1.

## Requisitos y escenarios de aceptación

### REQ-SV-01 — Verificar antes de cerrar y avanzar

Después del último cambio de implementación de cada slice, ejecutar su verificación pertinente
y los checks obligatorios del repositorio antes de marcarlo `verified` o avanzar al siguiente.
Se permiten pruebas durante el desarrollo, pero no sustituyen la comprobación del estado final.
Un cierre acumulado posterior no sustituye esta obligación por slice.

- Positivo: todos los criterios requeridos y comandos obligatorios pasan en el estado final;
  registrar evidencia y continuar con el siguiente slice autorizado sin nuevo permiso.
- Negativo: el código está escrito, pero falta una comprobación; no declarar `verified`.
- Interrupción: si se interrumpe el trabajo o falta infraestructura, preservar el estado
  incompleto y la acción pendiente; al retomar, verificar antes de continuar. No prometer que
  la verificación se ejecutará durante una interrupción forzada ni declarar un cierre ficticio.

### REQ-SV-02 — Evidencia atómica y trazable

Cada criterio requerido debe mapearse a uno o más ítems observables, identificables y
reproducibles. Separar comportamientos cuando uno pueda fallar aunque otro pase.
Un mismo test puede respaldar varios ítems si demuestra cada afirmación explícitamente.

Cada ítem registra criterio de origen, acción/entrada, esperado, método, observado y estado.
El registro del slice añade identificador, revisión del plan, fecha, estado de código evaluado,
comandos exactos con resultado de salida y referencias a evidencia pertinente. `HEAD` solo no
identifica cambios sin commit: debe acompañarse de una referencia reproducible al estado
afectado. No guardar secretos ni volcar logs completos.

- Positivo: mensaje visible y foco tienen comprobaciones separadas; ambos pasan con evidencia.
- Negativo: aparece el mensaje pero no cambia el foco; el ítem de foco queda `FAIL`.
- Negativo: el comando nunca se ejecutó, o solo existe una afirmación histórica; no es `PASS`.

### REQ-SV-03 — Estados inequívocos

Usar `PASS` cuando la evidencia vigente demuestra el criterio; `FAIL` cuando lo contradice;
`NO VERIFICADO` cuando falta evidencia suficiente. Las plantillas empiezan sin resultados
afirmados. Un fallo de infraestructura que impide observar el comportamiento no demuestra
un fallo funcional: registrar `NO VERIFICADO` y el error del check o bloqueo correspondiente.

No convertir un criterio requerido en «no aplica» para permitir el cierre. Las comprobaciones
genéricas que no correspondan pueden excluirse con justificación; cambiar un criterio requerido
exige el tratamiento del plan aprobado. Un aplazamiento explícitamente autorizado conserva su
razón y alcance, y nunca equivale a verificar el slice aplazado.

### REQ-SV-04 — Profundidad proporcional, obligación constante

Seleccionar comprobaciones desde los criterios y las superficies afectadas: límites y errores
de dominio cuando existan, contratos cuando cambien y regresiones de consumidores afectados.
Si el criterio trata UI, demostrarlo en la aplicación ejecutada, mediante automatización de
navegador o recorrido manual reproducible. Incluir teclado, foco y responsive cuando formen
parte del comportamiento requerido. Un test unitario no demuestra un submit real.

- Positivo: un cálculo se comprueba en sus límites; su presentación se comprueba en la UI.
- Negativo: lint y build pasan, pero nadie comprueba el cálculo; no se da por aceptado.
- Positivo: un cambio exclusivamente documental utiliza comprobaciones documentales pertinentes,
  además de todos los checks que el repositorio exija.

### REQ-SV-05 — Autoridad única y ubicación compatible

Conservar `09-delivery-status.md` como autoridad de entrega. Su cuerpo resume y enlaza
`slices/<SLICE-ID>.md`, donde reside el detalle; no copiar la tabla completa a ambos archivos.
Resolver la sesión desde el tracker seleccionado y comprobar su coherencia con la carpeta y
el plan. No usar literalmente `{session}` ni seleccionar otra sesión silenciosamente.

- Positivo: un lector abre el tracker y llega al detalle reproducible del slice.
- Negativo: el detalle contiene un criterio requerido fallido y el tracker dice `verified`;
  reportar inconsistencia y bloquear cierre, sin elegir el resultado más favorable.
- Compatibilidad: no fabricar checklists históricos ni asumir `PASS` al leer sesiones antiguas.
  Una nueva ejecución o reverificación registra evidencia actual bajo el contrato adoptado.

### REQ-SV-06 — Recuperación y vigencia

Ante un fallo recuperable, investigar, corregir dentro del alcance y repetir las comprobaciones
afectadas. Registrar reproducción, esperado, observado, impacto y ubicación cuando se conozca.
No repetir el mismo fallo sin un cambio relevante en código, entorno, datos o hipótesis.

Cualquier cambio posterior invalida la evidencia afectada y la de sus dependientes; ante
incertidumbre sobre el impacto, ampliar la reverificación. Escribir el propio reporte no
invalida automáticamente pruebas de código que no cambió. Sí deben repetirse los checks
documentales o globales que correspondan al nuevo estado de los archivos.

Un bloqueo real registra qué falta, qué se intentó y la condición para retomar. Una solicitud
de revisión no autoriza corregir código ni promover el estado de entrega; una consulta de
estado permanece de solo lectura.

### REQ-SV-07 — Cierre comprobable y límites de la garantía

La propuesta requiere un control determinista que rechace un cierre con criterios requeridos
ausentes, estados pendientes/fallidos, evidencia requerida sin referencia o checks obligatorios
sin resultado satisfactorio. Debe distinguir consistencia documental de verdad del comportamiento:
no afirmar que la primera certifica la segunda. La integración y el formato se definirán tras
Gate 1; no se prescribe una implementación desde este documento.

La verificación acumulada final conserva su alcance de regresión entre slices y comprueba que
no queden evidencias invalidadas, bloqueos o aceptaciones requeridas pendientes. `Complete`
describe solo el alcance autorizado, sin implicar release o despliegue.

## Evaluación futura de la mejora

Proteger los escenarios positivos y negativos anteriores con comprobaciones deterministas
pertinentes cuando se implemente el contrato. Evaluar cobertura y rechazo de estados
inconsistentes, no solo presencia de frases en la skill. La autoridad existente corresponde a
`project-plan-execution.execution` y `project-plan-execution.delivery-state` en
[authority-map.yaml](../../../authority-map.yaml).

Las pruebas de comportamiento con modelos requieren autorización explícita y una comparación
con el mismo modelo/runtime de referencia. Un caso aislado no demuestra una mejora general.
La suite sin credenciales valida los cambios documentales de esta sesión; no demuestra todavía
que el agente aplicará el futuro protocolo en una entrega real.
