# Diseño técnico — Verificación de slices

Status: Approved
Last updated: 2026-09-14

## Confirmed

Gate 1 fue aprobado explícitamente el 2026-09-14. Este documento implementa conceptualmente
los requisitos aprobados; todas las operaciones, campos y archivos nuevos descritos abajo
son propuestas, todavía no existen como capacidades del producto.

La distribución actual incluye el manifiesto y `skills/`, no el paquete Python de calidad:
[packaging.py](../../../src/devquitect_quality/packaging.py). El validador permite recursos
enlazados directamente desde cada `SKILL.md`:
[validate.py](../../../src/devquitect_quality/validate.py). Los snapshots recogen los archivos
de `skills/`: [sources.py](../../../src/devquitect_quality/sources.py).
Python 3.12 y PyYAML 6 ya forman parte del entorno de desarrollo del repositorio.

## Assumptions

- Un solo escritor por sesión, como exige el contrato actual; no se añade un servicio ni locks.
- El consumidor que adopte el control dispone de Python 3.12+ y PyYAML 6.x. La skill comprueba
  su disponibilidad; si faltan, informa el requisito y no instala nada automáticamente.
- El agente y la persona que aprueba el plan siguen siendo responsables de que los criterios
  cubran el comportamiento real y de la autenticidad de las observaciones.

## Open decisions

Ninguna decisión técnica bloqueante pendiente. El usuario aprobó Gate 2 el 2026-09-14,
incluido el requisito de runtime del consumidor. No se ha autorizado implementación.

## Componentes y autoridad

| Componente | Responsabilidad y decisión |
| --- | --- |
| Plan aprobado | Criterios, dependencias, comandos requeridos y alcance de entradas que pueden afectar cada slice |
| `references/execution.md` | Secuencia obligatoria implementar → verificar → corregir → cerrar; métodos de prueba proporcionales |
| `references/delivery-state.md` | Estado, referencias de evidencia, compatibilidad y recuperación |
| `slices/<SLICE-ID>.md` | Único detalle estructurado de la verificación actual del slice |
| Script propuesto `skills/project-plan-execution/scripts/verify_slice.py` | Identificar entradas, validar evidencia y ejecutar la transición de cierre de un slice |
| `09-delivery-status.md` | Único checkpoint de entrega; estado y enlace al detalle, sin copiar todos los criterios |
| Tooling del repositorio | Probar el script, los contratos y su inclusión en snapshots/paquetes |

El script se enlaza directamente desde el entrypoint para cumplir la allowlist actual.
No se importa `devquitect_quality` desde el script distribuido: ese módulo no viaja con el
plugin. Se reutilizan PyYAML y biblioteca estándar, sin framework de comandos ni parser YAML
propio. La documentación detallada del nuevo formato pertenece a una referencia de la skill,
también enlazada directamente desde su entrypoint.

Se mantienen los propietarios de los dos contratos existentes del mapa de autoridad.
El nuevo contrato `project-plan-execution.slice-close-guard` tendrá al script como `owner_path`
de las invariantes deterministas y formato aceptado; su referencia documental será `explains`,
el entrypoint `routes` y sus casos `tests`, roles existentes del esquema. La secuencia de
ejecución y estado siguen bajo sus propietarios actuales. No añadir un rol `implements` ni
repartir la misma regla completa entre varias referencias.

## Decisiones y alternativas

1. **Script distribuido con la skill.** Un comando exclusivo de `devquitect_quality` dejaría
   fuera al consumidor del plugin. Un servicio o hook específico de un host añadiría una
   dependencia externa al flujo. Se reconsideraría si el producto distribuye un runtime común.
2. **YAML en Markdown.** Conserva el formato de los checkpoints y evita otra base de estado.
   Se descarta parsear tablas libres como contrato de máquina y escribir un parser YAML propio.
   PyYAML es un requisito explícito en proyectos consumidores, aunque ya exista en este repo.
3. **Validación y cierre en el mismo script.** Un reporte consultivo no impide que el camino
   soportado escriba un estado inválido. `close` valida antes de escribir; `check` no modifica.
4. **Huella por alcance aprobado.** Detecta evidencia obsoleta sin invalidar pruebas por la
   edición del propio checklist. No convierte un hash en una copia recuperable del código.

## Contrato del plan

Los planes nuevos incorporan un único bloque cercado `devquitect-verification` con un mapping
YAML versionado. No es otro plan: vive dentro de `08-implementation-plan.md` y participa de
su revisión y aprobación. Los criterios de aceptación de cada slice tienen identificadores
estables y texto observable en este bloque; la prosa enlaza esos identificadores, sin mantener
otra lista normativa paralela. Los requisitos siguen siendo la autoridad del comportamiento.

El bloque contiene `schema_version: 1` y `slices`, indexado por `SLICE-*`. Cada entrada define:

- `criteria`: mapping de ID a texto observable y referencia al requisito; todos son requeridos.
- `checks`: mapping de ID a `command` y `cwd` relativo al repositorio; todos son obligatorios.
- `depends_on`: IDs existentes de slices del mismo plan.
- `inputs`: rutas relativas de archivos o directorios que influyen en las comprobaciones,
  incluyendo tests, configuración, lockfiles, consumidores y fuentes compartidas pertinentes.

Los directorios se expanden recursivamente; no se introduce un lenguaje de globs. El alcance
conservador por defecto es la raíz del repositorio. Una selección menor requiere justificación
en el plan. Checks impuestos por `AGENTS.md` deben incorporarse antes de aprobarlo; si una
instrucción cambia después, no se acepta el inventario antiguo como excepción a la nueva regla.
Rechazar IDs duplicados, dependencias inexistentes y ciclos; no seleccionar silenciosamente
una parte válida de un contrato malformado.

El verificador puede comparar IDs y resultados; no puede descubrir automáticamente que un
requisito en lenguaje natural se omitió del inventario. Esa completitud se revisa en el plan
y se protege con casos externos de la skill.

## Contrato del detalle por slice

Cada `slices/<SLICE-ID>.md` usa frontmatter YAML con `schema_version: 1`, `session`, `slice`,
`plan_revision`, `plan_digest`, `verified_at`, `inputs_digest`, `environment`, `criteria`
y `checks`. Las colecciones se indexan por los IDs del plan; duplicados son error, no
sobrescritura silenciosa de YAML. El cuerpo conserva notas y bloqueos, no otra tabla normativa.

Cada criterio contiene `action`, `expected`, `method`, `observed`, `status` y `evidence`.
`evidence` referencia un check declarado o una referencia manual local con procedencia,
fecha y pasos reproducibles. La observación debe ser no vacía para `PASS` o `FAIL`.
`NO VERIFICADO` permite ausencia de resultado y exige explicar qué falta.
Se conservan exactamente los estados aprobados; el verificador no infiere `PASS` del texto.

Cada check contiene el comando y directorio exactos del plan, `started_at`, `finished_at`,
`exit_code`, `status`, `observed`, `inputs_before` e `inputs_after`. Un check incompleto puede
tener salida nula y `NO VERIFICADO`; para cierre requiere `PASS`, salida cero y huellas iguales
a la huella vigente. Una comprobación manual usa los campos del criterio y no inventa un
comando exitoso. Fechas son ISO 8601 con zona; tipos, IDs y referencias se validan estrictamente.

El script presenta un resumen legible y puede emitir la tabla de criterios como vista por
stdout. No guarda una segunda tabla editable ni un archivo JSON paralelo de estado.
Logs extensos permanecen fuera del checkpoint; las referencias locales requeridas deben existir.
No se descargan URLs ni se ejecutan comandos encontrados en la evidencia.

## Identidad del estado y vigencia

`plan_digest` es SHA-256 de los bytes del plan aprobado; un cambio de revisión o contenido
impide reutilizar el detalle sin reconciliarlo. No se infiere aprobación de ese hash.

La huella de entradas usa un inventario ordenado de rutas normalizadas, tipo, modo ejecutable
y SHA-256 de contenido. Incluye archivos Git tracked y untracked no ignorados bajo los
directorios declarados, archivos ignorados declarados explícitamente y marcas de ausencia
para archivos eliminados. Volver a expandir el inventario detecta adiciones y eliminaciones.

Excluir únicamente los checkpoints operativos de la sesión y `slices/` de esa sesión; incluir
el resto de las definiciones cuando caen dentro del alcance. `.git/` nunca es entrada. Salidas
generadas deben estar ignoradas o fuera de las entradas, según el plan, y no pueden excluirse
fuentes necesarias solo para estabilizar el hash. Referencias a evidencia se comprueban aparte.

La primera versión rechaza entradas especiales, symlinks y submódulos dentro del alcance:
no seguirlos ni certificar contenido no identificado. Informar la ruta y la limitación para
ajustar el alcance legítimamente o ampliar el soporte; nunca convertir el error en `PASS`.
El comando falla claramente fuera de un repositorio Git. Estas limitaciones deben documentarse
antes de que una entrega adopte el control.

`snapshot` calcula la huella antes y después de comprobar. Si una prueba modifica entradas,
la evidencia no sirve para cierre hasta repetir sobre un estado estable. Un cambio en entradas
compartidas invalida los slices afectados y sus dependientes. Se preservan slices cuyo alcance
y evidencia permanecen vigentes. Cambios en servicios remotos, datos o runtime requieren
reverificación por impacto: el hash de archivos no los detecta; `environment` declara runtime,
configuración no secreta y versión o referencia externa relevante.

## Interfaz propuesta

Desde cualquier proyecto consumidor, usando la ruta real del script de la skill instalada:

```text
python <skill-root>/scripts/verify_slice.py snapshot --session <directory> --slice <SLICE-ID>
python <skill-root>/scripts/verify_slice.py check --session <directory> --slice <SLICE-ID>
python <skill-root>/scripts/verify_slice.py close --session <directory> --slice <SLICE-ID> --expected-revision <N>
```

`snapshot` devuelve identidad de plan y entradas, sin afirmar aceptación. `check` verifica
precondiciones, cobertura, estados, checks, vigencia y contradicciones del tracker; es de solo
lectura. `close` aplica la misma validación y, únicamente si pasa, actualiza ese slice a
`verified` y enlaza `slices/<SLICE-ID>.md`. No ejecuta tests: debe recibir evidencia de la
ejecución real realizada por el agente. No instala, usa red ni ejecuta shell desde datos.

Salida: JSON por stdout con `schema_version`, `operation`, `session`, `slice`, `result`,
`inputs_digest` y `issues` con código, ruta/campo y mensaje. Errores de runtime legibles por
stderr. Exit `0`: operación válida; `1`: criterios/estados/evidencia impiden aceptación;
`2`: formato, versión, ruta, runtime, soporte o conflicto de revisión impiden evaluar/escribir.
Una revisión o consulta de estado nunca utiliza `close`.

## Transición de cierre y recuperación

Antes de cerrar, comprobar Gate 1 y Gate 2 aprobados, definición completa, plan Approved y
revisión coincidente, slice autorizado, dependencias satisfechas y ninguna aceptación requerida
pendiente. Las autorizaciones declaradas en archivos no se autentican: la skill conserva la
responsabilidad de vincularlas con la instrucción real del usuario.

El cierre permitido parte de `in-progress` o `implemented`; no salta desde `pending`,
`blocked`, `invalidated` o `deferred`. Una repetición sobre `verified` solo es idempotente si
su evidencia sigue válida: no incrementa revisión ni rehabilita evidencia obsoleta.

`close` recuerda bytes y revisión del tracker, valida, recalcula entradas y vuelve a leer los
archivos antes de escribir. Si cambió el tracker, plan o evidencia, termina con conflicto.
Actualiza frontmatter y una sección delimitada de resumen de cierre en el cuerpo, conservando
el resto del cuerpo y todos los campos ajenos. Serializar YAML puede normalizar su formato;
comentarios dentro del frontmatter no son almacenamiento autoritativo.

La escritura usa archivo temporal en el mismo directorio y reemplazo atómico, sin commits ni
locks. Solo un escritor está soportado; la comprobación de revisión detecta conflictos
observados, no promete exclusión mutua ante escritores simultáneos.

Incrementa `revision` una vez, refresca fecha, limpia `current_slice` y mantiene entrega activa
con una acción concreta: seleccionar el próximo slice autorizado listo o ejecutar la revisión
acumulada si no quedan slices pendientes. No declara entrega `complete`: conserva la revisión
final y aceptaciones del contrato existente. No borra bloqueos ajenos ni amplía autorizaciones.

Si hay fallo, no escribe `verified`; el agente corrige y reintenta con evidencia nueva.
Si ya había un `verified` cuya evidencia quedó obsoleta, `check` reporta la inconsistencia y
el flujo de recuperación marca los afectados `invalidated`, sin reparar durante una consulta.
Una interrupción antes del reemplazo conserva el tracker anterior; después conserva un
checkpoint íntegro. No hay un segundo estado que reconciliar.

## Compatibilidad, adopción y reversión

No cambia la ubicación ni las versiones actuales de `00-status.md` y `09-delivery-status.md`.
La referencia `evidence` por slice es un campo opcional adicional en el tracker; su ausencia
en sesiones antiguas no invalida lecturas de estado. El formato de evidencia tiene su versión
independiente. No inicializar delivery desde esta fase de definición.

Los planes nuevos incluyen el contrato estructurado al aprobarse. Un plan antiguo sigue
consultable; para ejecutar nuevos slices con este control se incorpora el inventario al plan,
se incrementa su revisión y se solicita su aprobación según el flujo existente. No se completa
esa migración silenciosamente ni se fabrica evidencia histórica. Un cambio puramente documental
de adopción se analiza por impacto para preservar los slices no afectados.

Si faltan runtime o contrato, no hay fallback a cierre manual declarado equivalente. El agente
informa el requisito concreto y mantiene el trabajo sin verificar hasta resolverlo. Instalar
dependencias requiere la autorización correspondiente, incluso si Gate 2 aprobó su diseño.

Revertir una adopción preserva plan, evidencia y tracker; requiere una decisión explícita de
política y reevaluar el contrato aplicable. Una skill antigua puede ignorar el nuevo campo:
volver a ella no conserva la garantía del camino de cierre nuevo y debe reportarse así.

## Límites del control

El script garantiza que su operación `close` no acepta registros que incumplan las reglas
deterministas. No impide que una persona o agente edite Markdown directamente por otro medio.
Bloquear esas escrituras exigiría permisos de filesystem o integración obligatoria del host,
fuera del alcance aprobado. No se afirma esa garantía global.

Tampoco demuestra que un comando declarado se ejecutó, que una captura no fue manipulada,
que una lista de criterios es completa o que el entorno externo sigue igual. Tests reales,
revisión y casos de comportamiento complementan el control documental. No se usan firmas,
servicios de atestación ni un runner arbitrario de comandos para simular esa certeza.

## Trazabilidad y verificación de implementación

| Requisito | Tratamiento técnico | Evidencia futura mínima |
| --- | --- | --- |
| REQ-SV-01 | `close` valida antes de la transición; ejecución por slice | Camino válido cierra; check faltante no escribe; no avanza tras fallo |
| REQ-SV-02 | Inventario aprobado y detalle por ID | Detectar criterio omitido, duplicado, referencia rota y check indirecto no suficiente |
| REQ-SV-03 | Estados y tipos estrictos | Rechazar `FAIL`, `NO VERIFICADO`, salida nula o no cero al cerrar |
| REQ-SV-04 | Métodos adecuados y comandos aprobados | Casos de skill distinguen UI, dominio y checks técnicos; no imponer navegador a documentación |
| REQ-SV-05 | Tracker único y enlace al detalle | Roundtrip sin pérdida de cuerpo/campos; status legacy de solo lectura |
| REQ-SV-06 | Huellas, revisión y recuperación | Cambio de fuente/plan invalida; escribir checklist no altera huella; conflicto no escribe |
| REQ-SV-07 | Validador compartido por `check` y `close` | Mismos rechazos; dependencia o aceptación pendiente bloquea; fallo no deja tracker parcial |

Pruebas adicionales de límites: rutas escapadas, symlinks, claves YAML duplicadas, versiones
desconocidas, instalación de skill sin el repo de calidad, runtime ausente y doble cierre.
Probar snapshots/paquetes con el script referenciado y sin imports al tooling del repositorio.
La prueba de completitud semántica del inventario y la de método pertinente pertenecen a los
casos de la skill; no atribuirlas al parser determinista.

Durante implementación se ejecutarán la suite sin credenciales, Ruff y `git diff --check`,
además de las pruebas específicas del verificador. Las pruebas con modelos requieren permiso
explícito y baseline estable. La revisión de este documento no demuestra el futuro runtime.

## Gate 2

Responsabilidades, datos, interfaz, transiciones, errores, compatibilidad, runtime y límites
están definidos y los siete requisitos tienen tratamiento técnico. No hay servicios externos
ni dependencias nuevas para desarrollar en este repositorio. El requisito PyYAML en consumidores
es una consecuencia visible de distribuir un script que lee los checkpoints existentes.

Gate 2 fue aprobado para elaborar el plan de implementación. No se
modifica aún el System Context: el diseño propuesto no es una capacidad implementada.
