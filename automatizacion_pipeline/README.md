# Apache Airflow – DAGs Funcionales y Automatización de Pipelines

Este repositorio contiene la implementación de **DAGs funcionales en Apache Airflow**, desarrollados como ejercicios prácticos para comprender la creación, ejecución y monitoreo de workflows basados en **grafos dirigidos acíclicos (DAGs)**.

El proyecto fue desplegado utilizando **Apache Airflow 2.9.3 sobre Docker en Windows**, siguiendo buenas prácticas de configuración, diagnóstico y orquestación de pipelines.

---

## 📌 Objetivo del ejercicio

- Instalar y configurar Apache Airflow.
- Crear DAGs con múltiples tareas.
- Definir dependencias simples y complejas entre tareas.
- Ejecutar y monitorear DAGs desde la interfaz web.
- Verificar logs de ejecución.
- Comprender el uso de operadores básicos de Airflow.

---

## 🛠️ Tecnologías utilizadas

- **Python 3.12**
- **Apache Airflow 2.9.3**
- **Docker & Docker Compose**
- **PostgreSQL 15**
- **Windows 11**

---

## 📁 Estructura del proyecto

```
airflow_docker/
├── dags/
│   ├── saludo_diario.py
│   ├── dependencias_complejas.py
│   ├── flujo_saludo_diario.png
│   ├── operadores_sensores.py
│   ├── operadores_sensores.png
│   ├── monitoreo_alertas.py
│   ├── monitoreo_alertas.png
│   └── README.md
└── docker-compose.yml
```

---

## 🚀 DAG 1: Saludo Diario

### Descripción

DAG introductorio que permite validar la correcta instalación y funcionamiento de Apache Airflow.

- **DAG ID**: `saludo_diario`
- **Schedule**: `@daily`
- **Catchup**: deshabilitado

### Flujo de ejecución

```
tarea_bash → tarea_python → tarea_esperar
```

### Resultado esperado

- Ejecución secuencial de las tareas.
- Visualización correcta del flujo en Graph View.
- Logs accesibles desde la interfaz web.

---

## 🧩 DAG 2: Pipeline de Ventas con Dependencias Complejas

Como parte del ejercicio de automatización, se implementó un DAG que modela un **pipeline ETL de ventas**, incorporando ejecución paralela y sincronización explícita entre tareas.

- **DAG ID**: `pipeline_ventas_complejo`
- **Schedule**: `@daily`
- **Catchup**: deshabilitado

---

### 1️⃣ Visualización del grafo de dependencias

El DAG fue visualizado utilizando **Graph View** en la interfaz web de Apache Airflow, permitiendo verificar visualmente el flujo de ejecución y las dependencias entre tareas.

**Flujo verificado:**

```
preparar_entorno → [extraer_api_ventas, extraer_db_productos]
extraer_api_ventas → validar_datos_api → transformar_ventas ↘
extraer_db_productos → validar_datos_db → transformar_productos ↘
                                   join_ventas_productos
                                             ↓
                                    cargar_data_warehouse
                                             ↓
                                   enviar_reporte_ejecucion
```

El grafo confirma ejecución paralela en las etapas de extracción y validación, seguida de una sincronización explícita en la etapa de *join* antes de la carga final.

---

### 2️⃣ Pruebas de ejecución del DAG

Para validar el correcto funcionamiento del pipeline se realizaron los siguientes escenarios:

**Prueba del DAG sin scheduler:**
```bash
airflow dags test pipeline_ventas_complejo 2024-01-01
```

**Ejecución manual del DAG:**
```bash
airflow dags trigger pipeline_ventas_complejo
```

**Revisión de logs de la tarea final:**
```bash
airflow tasks logs pipeline_ventas_complejo enviar_reporte_ejecucion 2024-01-01
```

Los logs confirman que el pipeline se ejecuta correctamente hasta la generación del reporte final.

---

### 3️⃣ Verificación conceptual

**a) Elección entre PythonOperator y BashOperator**

El `PythonOperator` se utiliza cuando la tarea requiere lógica de negocio, procesamiento de datos o validaciones mediante código Python.  
El `BashOperator` es más adecuado para ejecutar comandos del sistema operativo o tareas simples de preparación del entorno, como la creación de directorios o ejecución de scripts shell.

**b) Ventajas de definir dependencias explícitas**

Definir dependencias explícitas permite ejecutar tareas en paralelo, representar claramente el flujo mediante un grafo acíclico, evitar ejecuciones incorrectas y facilitar el monitoreo, debugging y mantenimiento del pipeline.

---

### ✅ Resultados

- DAGs cargados correctamente sin errores.
- Ejecuciones exitosas de todas las tareas.
- Dependencias simples y complejas correctamente definidas.
- Visualización y monitoreo desde Airflow Web UI.
- Logs accesibles para validación de ejecución.

---

### 🧠 Conclusiones

El desarrollo de estos DAGs permitió consolidar los conceptos fundamentales de Apache Airflow, incluyendo la definición de workflows, uso de operadores, paralelismo, dependencias complejas y monitoreo de ejecuciones en un entorno Docker.

---
## 📂 DAG 3: Pipeline con Sensores y Operador Personalizado

Este DAG incorpora **sensores y operadores personalizados**, simulando un escenario real de ingesta de datos dependiente de eventos externos.

- **DAG ID**: `pipeline_con_sensores_y_operador_custom`
- **Schedule**: `@hourly` (ejecutado manualmente durante pruebas)
- **Catchup**: deshabilitado

### Flujo del DAG
```
esperar_archivo_datos
        ↓
validar_datos_ventas
        ↓
procesar_datos_ventas
        ↓
generar_reporte
        ↓
limpiar_archivos
```

---

### 🧠 Verificación conceptual

**¿Cuándo usar sensores?**  
Se utilizan sensores cuando la ejecución de un pipeline depende de una condición externa, como la llegada de archivos o la disponibilidad de datos.

**¿Ventajas de operadores personalizados?**  
Permiten encapsular lógica de negocio específica, mejorar la reutilización de código y mantener DAGs más limpios.

## DAG 4: Pipeline con Monitoreo y Verificación Conceptual

Este DAG está orientado a monitoreo avanzado, métricas y alertas, simulando un pipeline productivo donde no solo importa ejecutar tareas, sino medir su comportamiento y reaccionar ante incidentes.

DAG ID: pipeline_monitorado

Schedule: ejecución manual (durante pruebas)

Catchup: deshabilitado

### Flujo del DAG
```
procesar_datos
        ↓
validar_metricas
        ↓
notificar_exito
        ↓
verificar_sla
```

---


## 🧠 Verificación conceptual
🔹 ¿Qué métricas son más importantes para monitorear en un pipeline de datos?

Las métricas clave dependen del objetivo del pipeline, pero en un entorno productivo las más relevantes suelen ser:

Estado de las tareas (success / failed / retry)
Permite detectar fallos operacionales de forma inmediata.

Duración de ejecución por tarea y por DAG
Ayuda a identificar cuellos de botella y degradaciones de rendimiento.

Cumplimiento de SLA
Fundamental para pipelines críticos que alimentan procesos de negocio o reporting.

Volumen de datos procesados
Permite detectar anomalías (datos incompletos, duplicados o caídas abruptas).

Errores funcionales o de validación
Indicadores de problemas en la calidad de los datos.

🔹 ¿Cómo decidir entre enviar alertas por Email vs Slack vs SMS?

La elección del canal de alertas debe basarse en criticidad, urgencia y contexto operativo:

Canal	Cuándo usarlo
Email	Alertas informativas, reportes de éxito, fallos no críticos o resúmenes diarios.
Slack / Teams	Incidentes operativos que requieren atención rápida del equipo técnico. Ideal para entornos colaborativos.
SMS	Fallos críticos en pipelines productivos, SLA incumplidos o eventos que requieren acción inmediata fuera del horario laboral.

Buena práctica:
Combinar canales según severidad (por ejemplo, email para éxito, Slack para warnings y SMS para errores críticos).

### ✅ Resultados del DAG 4

Pipeline ejecutado correctamente.

Métricas registradas y evaluadas.

Alertas configuradas sin interrumpir el flujo principal.

Separación clara entre lógica de negocio y monitoreo.

### 🧠 Conclusión general

Con este cuarto DAG se completa un enfoque integral de Apache Airflow:

Orquestación básica, Dependencias complejas, Sensores y operadores personalizados, Monitoreo, métricas y alertas

---

## Verificación conceptual – Manejo de errores en pipelines

### ¿Qué diferencia hay entre un pipeline que falla silenciosamente y uno con buen manejo de errores?

Un pipeline que falla silenciosamente no registra ni comunica los errores ocurridos durante su ejecución, lo que puede provocar que el flujo continúe procesando datos inválidos o incompletos. Esto dificulta el monitoreo, el debugging y la detección de fallos, aumentando el riesgo de generar resultados incorrectos sin que el problema sea evidente.

En contraste, un pipeline con buen manejo de errores detecta y captura explícitamente las excepciones, registra información clara sobre el fallo y detiene la ejecución cuando un error crítico compromete la calidad del dato. Este enfoque mejora la confiabilidad, trazabilidad y mantenibilidad del pipeline.

---

### ¿Cómo decidir cuándo reintentar versus abortar una ejecución?

La decisión depende del tipo de error y su impacto en los datos:

- **Reintentar la ejecución** es adecuado cuando el error es transitorio, como fallas temporales de red, timeouts de APIs externas o problemas momentáneos de infraestructura.
- **Abortar la ejecución** es necesario cuando el error es lógico o crítico, como fallas de validación, esquemas incorrectos o datos corruptos, ya que continuar podría propagar datos inválidos a etapas posteriores.

Un pipeline robusto debe aplicar reintentos únicamente a errores transitorios y detener la ejecución ante errores que afecten la calidad o consistencia de los datos.

## 📌 Autor

**Fabián Díaz**  
Proyecto de aprendizaje en Ciencia de Datos / Data Engineering.
