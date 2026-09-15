# Historial — Slice verification

## 2026-09-14 — Semilla, investigación y dirección propuesta

El usuario aportó un protocolo de verificación por slice: checklist con criterio, entrada,
esperado, método, observado y estado; cobertura de límites/UI; reparación de fallos;
reverificación después de cambios; prohibición de cerrar con criterios fallidos o no verificados.
Su ejemplo pedía guardar el checklist en `docs/software-design/{session}/slices/` y repetir
una tabla de evidencia en `09-delivery-status.md`.

Solicitó software-idea-to-project en modo persistente, contrastar el enfoque con OpenSpec y
evaluar si convendría separar diseño y ejecución en carpetas diferentes. Se revisaron el
System Context, las referencias de definición y entrega, el mapa de autoridad y la
documentación oficial de OpenSpec. La consulta de graphify devolvió principalmente nodos de
la infraestructura de evaluación; los contratos Markdown fueron la evidencia decisiva para
las rutas y estados de ejecución.

Se detectó la sesión relacionada `instruction-governance`; el usuario eligió explícitamente
crear una sesión distinta llamada `slice-verification`. También confirmó: «siempre se
verifique al terminar de trabajar un slice» y pidió una opinión crítica sobre su viabilidad.

Recomendación: preservar la carpeta por iniciativa; separar responsabilidades mediante el
tracker y detalle enlazado; hacer obligatoria la verificación antes del cierre de cada slice;
elegir pruebas proporcionales sin omitir requisitos ni checks del repositorio. Conservar la
verificación acumulada final. Evitar prellenar `PASS` y exigir tratamiento de evidencia obsoleta.

La comparación y opinión están en `01-concept.md`; los escenarios contrastables en
`02-requirements.md`. Se propone un control determinista de consistencia de cierre, sin
atribuirle capacidad para certificar la verdad semántica de evidencia declarada.

Clasificación: inicio de una definición de cambio al sistema, entrada de definición, modo
persistente; perfil confirmado de impacto acotado y profundidad estándar. Interacción mínima
centrada en lectura de estados, bloqueos y recuperación. Las sesiones previas no se reabren.

El usuario autorizó persistencia y confirmó un requisito, no la aprobación completa de Gate 1
ni implementación. Los documentos se presentaron en Review; la sesión quedó esperando Gate 1.

## 2026-09-14 — Gate 1 aprobado

Después del resumen de alcance, el usuario indicó: «Apruebo gate 1».
Se aprueban concepto y requisitos y se inicia diseño técnico. Esta aprobación no autoriza
implementar ni crear un plan antes de Gate 2. Se mantienen los límites y el alcance aprobados.

## 2026-09-14 — Arquitectura presentada a Gate 2

La inspección de packaging, snapshots y allowlist confirma que los recursos enlazados de la
skill pueden distribuirse; el módulo de calidad del repositorio no forma parte del plugin.
Se propone un script dentro de project-plan-execution con Python 3.12 y PyYAML 6, requisitos
ya disponibles en desarrollo y explícitos para consumidores. No se instalarán automáticamente.

Se elige YAML estructurado dentro de los documentos, inventario de criterios aprobado en el
plan, huellas de entradas y operaciones snapshot/check/close. La operación close valida antes
de escribir atómicamente el tracker; la revisión conserva check de solo lectura. No se añade
servicio, JSON de estado paralelo, hook de host ni runner que ejecute comandos desde evidencia.

Quedan documentadas las limitaciones: un escritor por sesión; Git requerido; symlinks y
submódulos del alcance no soportados en la primera versión; el hash no autentica observaciones
ni entornos remotos. La adopción en planes anteriores necesita revisión/aprobación del plan,
sin reconstruir resultados históricos. No se promete impedir ediciones directas al tracker.

El perfil sigue siendo acotado y estándar: se concretan superficies de datos, interfaz y
compatibilidad, sin cambiar el comportamiento aprobado ni requerir migración masiva.
Los siete requisitos tienen tratamiento y casos de verificación en 04-architecture.md.
Gate 2 queda pendiente; no se creó plan ni se implementó el script.

## 2026-09-14 — Gate 2 aprobado

Tras explicar el script adicional, las operaciones snapshot/check/close y los requisitos
Python/PyYAML, el usuario indicó: «Autorizo gate 2». Se aprueba la arquitectura y se inicia
el plan. No se interpreta esta aprobación como autorización para implementar o instalar.

## 2026-09-14 — Plan preparado para aprobación

El usuario pidió continuar; se retomó el checkpoint activo de planificación sin reiniciar
la definición. Se preparó 08-implementation-plan.md, revisión 1, con dos slices: verificador
distribuible y cierre protegido; integración del protocolo en planificación y ejecución.

El plan incorpora criterios identificados, checks concretos y alcance de entradas en el
formato estructurado aprobado. Distingue rutas existentes de propuestas, pruebas sin modelos
de evidencia end-to-end todavía no medida, actualización del System Context después de cada
capacidad verificada y la reverificación si el segundo slice afecta evidencia del primero.

Se verificaron las rutas del tooling, la allowlist y las aserciones de evaluación existentes.
No se implementó el script ni se crearon fixtures, tests o un checkpoint de entrega.
El plan queda en Review; ambas puertas de diseño permanecen aprobadas.

## 2026-09-14 — Plan aprobado; implementación no autorizada

El usuario indicó: «apruebo el plan, no lo implementes aun».
Se marca el plan revisión 1 como Approved y la definición como completa, conservando ambos
gates aprobados. No hay slices autorizados ni se crea 09-delivery-status.md. Cualquier ejecución
requiere una autorización posterior explícita; la aprobación del plan no la sustituye.
