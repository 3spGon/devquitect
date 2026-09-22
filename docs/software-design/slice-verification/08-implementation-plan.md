# Plan de implementación — Slice verification

Status: Approved
Last updated: 2026-09-14
Plan revision: 1

## Confirmed

Gate 1 y Gate 2 están aprobados. El alcance viene de [concepto](01-concept.md),
[requisitos](02-requirements.md) y [arquitectura](04-architecture.md).
El usuario aprobó explícitamente este plan el 2026-09-14 y ordenó no implementarlo aún.
No se autoriza implementar ni instalar dependencias.

El repositorio usa Python 3.12, PyYAML, pytest y Ruff. Los recursos de una skill deben estar
enlazados directamente desde su entrypoint para pasar la allowlist. El producto distribuye
`skills/`; el ejecutable no puede importar módulos de `devquitect_quality`.

## Assumptions

Se entrega en dos slices verticales: primero un verificador utilizable y probado; después su
integración obligatoria en planificación y ejecución. Ambos conservan el alcance acotado,
profundidad estándar y superficies del [perfil](00-status.md).
No se incluye un runner de pruebas: el agente ejecuta y registra los checks.

## Open decisions

Ninguna decisión técnica pendiente. El plan está aprobado.
La implementación requiere una autorización posterior que identifique SLICE-001, SLICE-002
o todo el plan; ninguna aprobación anterior se interpreta como esa autorización.

## Resultado y restricciones comunes

Un slice solo se cierra mediante la operación soportada después de verificar su estado final.
La evidencia se guarda por slice y el tracker mantiene el estado y enlace, sin tablas duplicadas.
Se preservan lectura legacy, autorizaciones, aceptación humana cuando sea requerida y revisión
acumulada final. No cambiar otras sesiones ni la política de publicación.

Sin commits, tags, instalaciones, publicaciones o despliegues. Las pruebas aisladas existentes
pueden construir repositorios temporales como ya hace test_packaging; eso no autoriza commits
en el checkout de trabajo. No cambiar versión del plugin ni ejecutar release-check como parte
de esta entrega local. La elegibilidad futura exige evidencia del commit candidato exacto y
autorizaciones independientes.

La lista de criterios normativa de este plan es el bloque al final. Sus IDs enlazan a los
requisitos de 02-requirements.md. Las secciones siguientes describen trabajo y pruebas, no
mantienen otra lista paralela de aceptación.

## SLICE-001 — Verificador distribuible y cierre protegido

**Resultado:** snapshot/check/close utilizables en una sesión de prueba, con el formato aprobado,
validación determinista y escritura atómica. Dependencias: ninguna. Precondiciones: aprobación
del plan, autorización explícita de este slice y entorno Python/PyYAML disponible.

**Archivos propuestos:**

- `skills/project-plan-execution/scripts/verify_slice.py`: las tres operaciones y lógica compartida.
- `skills/project-plan-execution/references/slice-verification.md`: formato, comandos y límites.
- `tests/unit/test_slice_verification.py`: casos deterministas con archivos y tracker temporales.

**Archivos existentes a modificar:**

- `skills/project-plan-execution/SKILL.md`: enlaces directos al script y referencia; en este
  primer slice explicar uso explícito sin anunciar aún integración obligatoria del flujo.
- `authority-map.yaml`: contrato slice-close-guard con script owner y referencias/entrypoint/tests
  en los roles aprobados; preservar contratos existentes.
- `tests/unit/test_sources.py`, `tests/unit/test_validate.py`, `tests/unit/test_packaging.py`:
  verificar inclusión del recurso, límites y uso sin importar el tooling de calidad.
- `docs/software-design/system-context.md`: actualizar capacidades y runtime del verificador
  solo después de implementarlo y verificarlo.

**Trabajo e interfaces:** implementar exactamente el contrato de 04-architecture.md.
Leer YAML con claves duplicadas rechazadas y carga segura; validar tipos y referencias,
inventario del plan, estados y huellas. Compartir la validación entre check y close para que
un fallo no encuentre una ruta de escritura alternativa. snapshot no declara aceptación.
Ninguna operación ejecuta comandos tomados del YAML ni hace solicitudes de red.

close valida las autorizaciones documentadas y `--expected-revision`, conserva datos ajenos
y utiliza reemplazo atómico. El bloque de resumen del cuerpo queda delimitado por
`<!-- devquitect:slice-close:start -->` y `<!-- devquitect:slice-close:end -->`;
se crea si falta y se rechazan delimitadores duplicados o incompletos. Solo esa sección
generada puede sustituirse, junto con el frontmatter cuya normalización ya fue aprobada.

**Casos mínimos:** sesión válida; un criterio ausente; PASS parcial; salida no cero;
evidencia obsoleta; criterio desconocido; YAML duplicado; rutas absolutas/escapadas;
dependencia o aceptación pendiente; revisión concurrente; doble cierre; fallo antes de
reemplazar el archivo. Comparar los bytes del tracker antes/después de cada rechazo.
Cubrir altas/bajas de archivos y exclusión del propio reporte. Probar falta de PyYAML en
un proceso aislado, sin desinstalarlo del entorno del usuario. Probar symlinks/submódulos
y Git ausente como errores de soporte, no resultados satisfactorios.

**Verificación:** ejecutar CHECK-GUARD, CHECK-PACKAGE y todos los checks comunes declarados
en el bloque. CHECK-GUARD apunta a un archivo propuesto: solo se ejecuta después de crearlo.
Los tests de packaging usan repositorios temporales, sin construir ni promover un release real.
Después de cambiar código, ejecutar `graphify update .` si Graphify está disponible y revisar el diff.

**Documentación y reversión:** registrar capacidad standalone en System Context; no afirmar
que el segundo slice esté entregado. Para revertir, conservar evidencia de sesiones y retirar
la capacidad solo con autorización: un runtime ausente no habilita cierre manual equivalente.

**Evidencia de cierre:** resultados de los comandos, escenarios positivos/negativos, artefactos
incluidos y una ejecución aislada de las tres operaciones. Crear
`slices/SLICE-001.md` solamente durante la entrega autorizada; enlazarlo desde el tracker.

## SLICE-002 — Integrar la verificación obligatoria en las skills

**Resultado:** el flujo de definición prepara el inventario y la ejecución usa el verificador
para cerrar cada slice. Dependencia: SLICE-001 verificado y vigente. Requiere autorización
explícita de este segundo slice; completar el primero no la concede.

**Archivos existentes a modificar:**

- `skills/project-plan-execution/references/execution.md`: loop, método pertinente,
  reverificación, close obligatorio y revisión acumulada.
- `skills/project-plan-execution/references/delivery-state.md`: enlace evidence por slice,
  recuperación, lectura legacy y adopción explícita.
- `skills/project-plan-execution/SKILL.md`: routing y preflight de runtime, manteniéndolo breve.
- `skills/software-idea-to-project/references/implementation-planning.md`: inventario
  estructurado como parte del plan aprobado, IDs atómicos y comandos pertinentes.
- `skills/software-idea-to-project/references/artifacts.md`: detalle subordinado y enlaces;
  preservar 00-status como autoridad de definición y 09-delivery-status como autoridad de entrega.
- `authority-map.yaml`: reflejar referencias afectadas y casos para contratos críticos.
- `tests/unit/test_slice_verification.py`: ampliar escenarios legacy/adopción e integración.
- `tests/unit/test_cases.py`: cubrir descubrimiento y validez de los nuevos casos.
- `docs/software-design/system-context.md`: registrar el flujo integrado únicamente después
  de comprobarlo.

**Archivos propuestos:**

- `evals/fixtures/slice-verification/`: sesión mínima aprobada de prueba con criterios y
  comandos locales reproducibles, sin secretos, runtimes externos ni resultados PASS prefabricados.
- `evals/cases/slice-verification-positive.yaml`: camino autorizado de verificación y cierre.
- `evals/cases/slice-verification-negative.yaml`: intento de cerrar evidencia incompleta.
- `evals/cases/slice-verification-legacy-status.yaml`: consulta antigua estrictamente de lectura.

**Trabajo e interfaces:** usar el mismo formato e interfaz entregados en SLICE-001. Los planes
nuevos conservan los criterios normativos en el bloque estructurado; la prosa explica y enlaza.
Las plantillas de evidencia comienzan NO VERIFICADO, no PASS. La falta de runtime o inventario
es una condición que se informa y resuelve, nunca motivo para inventar resultados.

Una sesión antigua puede consultarse sin cambios. Adoptar el formato para nueva ejecución
requiere revisión de plan y aprobación según los contratos existentes. No migrar las otras
sesiones del repositorio como demostración. La revisión de solo lectura no usa close.

**Casos y cobertura:** los tests deterministas ejecutan el script sobre sesiones de prueba y
verifican los estados finales. Los casos YAML usan las aserciones existentes
`command-occurrence`, `command-prohibition`, `checkpoint-transition` y `git-clean`
según el escenario. Se comprueba su carga sin modelos. No confundir presencia de un comando
con su éxito ni matching de palabras en una skill con ejecución correcta del agente.

La selección de pruebas de UI frente a dominio y la completitud semántica del plan se
describen en casos de comportamiento. Su eficacia end-to-end queda sin medir hasta una
ejecución model-backed explícitamente autorizada sobre baseline estable. No introducir
nuevos tipos de aserción o una infraestructura de evaluación distinta para esta entrega.

**Verificación:** CHECK-GUARD, CHECK-PACKAGE, CHECK-CASES y checks comunes. Inspeccionar los
contratos en su owner_path y las referencias secundarias para eliminar duplicación.
Si el slice modifica código, ejecutar `graphify update .` si Graphify está disponible antes de la comprobación final.

**Documentación y reversión:** actualizar System Context después de verificar la integración,
conservando las limitaciones y la ausencia de publicación. Un retorno a una skill antigua
puede ignorar el contrato: no describirlo como reversión que mantiene las mismas garantías.

**Evidencia de cierre:** comandos, resultados de pruebas, cobertura de casos y límites no
medidos. Guardar `slices/SLICE-002.md` durante entrega, sin duplicar su tabla en el tracker.

## Arranque y revisión acumulada de esta entrega

El verificador todavía no existe: no intentar ejecutarlo mientras se aprueba este plan.
Al autorizar implementación, project-plan-execution inicializa el tracker mediante su contrato
actual. SLICE-001 se desarrolla y verifica primero con tests del repositorio; cuando el script
funcione, se usa contra el propio detalle para cerrar ese slice. No requiere un PASS previo
de sí mismo: check y close son la puerta posterior a sus pruebas.

Preparar los campos de evidencia de este plan antes del primer cierre, sin fabricarlos.
La adopción de este mismo plan no cambia su revisión si su bloque ya fue aprobado y no hay
cambio de contenido. Una corrección posterior del plan sí sigue las reglas de revisión.

Las huellas de estos slices cubren un conjunto conservador compartido de fuentes, tests,
contratos y configuración; excluyen el grafo generado, que no es entrada del verificador.
La huella del plan se calcula por separado. El segundo slice puede invalidar evidencia del
primero: reverificar y cerrar de nuevo el afectado antes de aceptar dependencias y completar
la entrega, sin pedir permiso para repetir comprobaciones dentro del alcance autorizado.

Actualizar System Context cambia entradas y debe preceder la ejecución final de checks y
captura de evidencia vigente. No registrar un cierre con la huella anterior a esa actualización.
Si aparece un cambio fuera de las entradas declaradas que afecta pruebas, ampliar el plan
mediante su revisión aprobada; no ocultarlo reduciendo la huella.

Antes de finalizar todo el alcance autorizado, ejecutar de nuevo checks relevantes a la suma
de cambios, revisar el diff acumulado y confirmar ausencia de fallos, bloqueos o aceptaciones
pendientes. Informar por separado cualquier slice no autorizado. Una revisión final no
reemplaza la verificación obligatoria al terminar cada slice.

## Inventario ejecutable del plan

Formato propuesto, derivado de Gate 2; no es código de aplicación. Los comandos de tests sobre
archivos propuestos serán ejecutables cuando el slice correspondiente los cree. Cada comando
debe terminar con exit 0; devquitect check además debe reportar result pass. Ruff debe indicar
All checks passed y git diff --check no debe reportar errores.

```devquitect-verification
schema_version: 1
slices:
  SLICE-001:
    depends_on: []
    criteria:
      AC-SV-001:
        text: "snapshot identifica el plan y entradas finales; check detecta criterios ausentes, duplicados, referencias inválidas y estados no satisfactorios sin escribir."
        requirement: REQ-SV-02
      AC-SV-002:
        text: "Cambiar, añadir o eliminar una entrada invalida evidencia; modificar únicamente el tracker o checklist no altera la huella de entradas."
        requirement: REQ-SV-06
      AC-SV-003:
        text: "close solo escribe verified con autorización declarada, dependencias, aceptación y evidencia válidas; rechazos y conflictos dejan el tracker intacto."
        requirement: REQ-SV-07
      AC-SV-004:
        text: "El cierre conserva campos ajenos y cuerpo fuera de su resumen, enlaza el detalle e incrementa revisión una vez; repetirlo sobre evidencia vigente es idempotente."
        requirement: REQ-SV-05
      AC-SV-005:
        text: "El script entrega los códigos 0/1/2 documentados, rechaza claves duplicadas, versiones y rutas inválidas, y no ejecuta comandos declarados en evidencia."
        requirement: REQ-SV-03
      AC-SV-006:
        text: "El script y referencia viajan en snapshots/paquetes; funciona fuera del repo de calidad con Python/PyYAML y diagnostica sus limitaciones sin instalar."
        requirement: REQ-SV-07
      AC-SV-007:
        text: "Se documenta en System Context solo la capacidad del script realmente implementada y verificada, sin anticipar la integración del segundo slice."
        requirement: REQ-SV-06
    checks:
      CHECK-FAST:
        command: "uv run devquitect check --source working-tree --report .devquitect-reports/check.json"
        cwd: "."
      CHECK-RUFF:
        command: "uv run ruff check src tests"
        cwd: "."
      CHECK-DIFF:
        command: "git diff --check"
        cwd: "."
      CHECK-GUARD:
        command: "uv run pytest tests/unit/test_slice_verification.py"
        cwd: "."
      CHECK-PACKAGE:
        command: "uv run pytest tests/unit/test_sources.py tests/unit/test_validate.py tests/unit/test_packaging.py"
        cwd: "."
    inputs:
      - "skills"
      - "src"
      - "tests"
      - "evals"
      - "schemas"
      - ".codex-plugin"
      - "authority-map.yaml"
      - "pyproject.toml"
      - "uv.lock"
      - "AGENTS.md"
      - "docs/software-design/system-context.md"
      - "docs/software-design/slice-verification/01-concept.md"
      - "docs/software-design/slice-verification/02-requirements.md"
      - "docs/software-design/slice-verification/04-architecture.md"
  SLICE-002:
    depends_on: ["SLICE-001"]
    criteria:
      AC-SV-008:
        text: "La ejecución exige verificar después del último cambio, corregir fallos recuperables y cerrar antes de avanzar; conserva la revisión acumulada final."
        requirement: REQ-SV-01
      AC-SV-009:
        text: "La definición de planes produce inventario estructurado con IDs estables, criterios atómicos, checks y entradas aprobados; no duplica criterios normativos."
        requirement: REQ-SV-02
      AC-SV-010:
        text: "El protocolo elige evidencia pertinente para UI y dominio, no confunde build/lint con aceptación y no impone navegador a cambios documentales."
        requirement: REQ-SV-04
      AC-SV-011:
        text: "Una consulta legacy no escribe ni fabrica evidencia; adoptar el formato requiere revisión aprobada del plan y conserva slices no afectados por el cambio."
        requirement: REQ-SV-05
      AC-SV-012:
        text: "FAIL, NO VERIFICADO y evidencia histórica no permiten verified; las plantillas no prellenan PASS ni borran requisitos como no aplicables."
        requirement: REQ-SV-03
      AC-SV-013:
        text: "La referencia de recuperación distingue invalidación, fallo recuperable, falta de runtime y bloqueo real; no autoriza instalaciones ni cierre manual equivalente."
        requirement: REQ-SV-06
      AC-SV-014:
        text: "Casos positivos y negativos externos son válidos y se cubren invariantes ejecutables sin modelos; cualquier afirmación sobre comportamiento del agente distingue evidencia pendiente."
        requirement: REQ-SV-07
      AC-SV-015:
        text: "System Context refleja el flujo integrado solo tras verificarlo; el informe final identifica alcance, limitaciones y ausencia de publicación."
        requirement: REQ-SV-01
    checks:
      CHECK-FAST:
        command: "uv run devquitect check --source working-tree --report .devquitect-reports/check.json"
        cwd: "."
      CHECK-RUFF:
        command: "uv run ruff check src tests"
        cwd: "."
      CHECK-DIFF:
        command: "git diff --check"
        cwd: "."
      CHECK-GUARD:
        command: "uv run pytest tests/unit/test_slice_verification.py"
        cwd: "."
      CHECK-PACKAGE:
        command: "uv run pytest tests/unit/test_sources.py tests/unit/test_validate.py tests/unit/test_packaging.py"
        cwd: "."
      CHECK-CASES:
        command: "uv run pytest tests/unit/test_cases.py tests/integration/test_eval_command.py"
        cwd: "."
    inputs:
      - "skills"
      - "src"
      - "tests"
      - "evals"
      - "schemas"
      - ".codex-plugin"
      - "authority-map.yaml"
      - "pyproject.toml"
      - "uv.lock"
      - "AGENTS.md"
      - "docs/software-design/system-context.md"
      - "docs/software-design/slice-verification/01-concept.md"
      - "docs/software-design/slice-verification/02-requirements.md"
      - "docs/software-design/slice-verification/04-architecture.md"
```

## Handoff

Este documento está Approved y la definición está completa. El usuario indicó no implementarlo
aún. Implementar requiere autorización posterior con SLICE-001, SLICE-002 o todo el plan. Esa autorización permitirá
crear el checkpoint de entrega y la evidencia, no instalar, publicar, hacer commits ni ejecutar
pruebas con modelos. Se entrega a project-plan-execution junto con los documentos aprobados,
AGENTS.md y los límites explícitos de la arquitectura.
