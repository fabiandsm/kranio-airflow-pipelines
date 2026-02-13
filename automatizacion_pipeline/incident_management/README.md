# 🚨 Gestión de Incidentes y Recuperación para Pipelines de Datos

Este módulo implementa un **runbook automatizado de respuesta a
incidentes** para pipelines de datos, simulando escenarios reales de
operación en producción.

Forma parte del repositorio **Kranio**, orientado a demostrar
capacidades prácticas en **Ingeniería de Datos**, operación de pipelines
y gestión de confiabilidad de datos.

------------------------------------------------------------------------

## 🎯 Objetivos de Aprendizaje

Este ejercicio permite:

1.  Aprender manejo de incidentes en producción.
2.  Comprender estrategias de recuperación automática.
3.  Entender la importancia de post‑mortems técnicos.
4.  Prepararse para escenarios de fallos y recuperación de sistemas.
5.  Aplicar prácticas reales de operación y confiabilidad de pipelines.

------------------------------------------------------------------------

## 📂 Estructura del módulo

``` text
incident_management/
├── README.md
├── examples/
│   └── simulate_incident.py
├── src/
│   └── incident_response/
│       ├── __init__.py
│       ├── post_mortem.py
│       └── runbook.py
└── tests/
    └── test_runbook.py
```

------------------------------------------------------------------------

## 🧠 Conceptos implementados

### ✅ Runbook automatizado

Define pasos claros y repetibles para responder a incidentes:

-   Identificación del incidente
-   Ejecución de acciones de recuperación
-   Verificación de resolución
-   Escalamiento automático si falla la recuperación

Esto reduce tiempos de reacción y evita decisiones improvisadas bajo
presión.

------------------------------------------------------------------------

### ✅ Tipos de incidentes simulados

Actualmente se modelan:

-   Pipeline caído
-   Degradación de calidad de datos
-   Problemas de performance

Cada incidente define:

-   Severidad
-   Tiempo máximo de respuesta
-   Pasos de recuperación
-   Política de escalamiento

------------------------------------------------------------------------

### ✅ Escalamiento automático

Si un incidente no se resuelve dentro del tiempo esperado, se activan
acciones de escalamiento como:

-   Notificar ingeniero líder
-   Escalar a manager técnico
-   Escalar a niveles superiores

Esto garantiza visibilidad y acción rápida ante fallos críticos.

------------------------------------------------------------------------

### ✅ Recuperación automática

Se simulan acciones típicas de recuperación en producción:

-   Verificación de servicios críticos
-   Validación de conectividad
-   Reinicio de componentes fallidos
-   Verificación de recuperación del pipeline
-   Monitoreo posterior a la recuperación

------------------------------------------------------------------------

### ✅ Template de Post‑Mortem

El módulo incluye generación de plantillas para documentar:

-   Timeline del incidente
-   Impacto técnico y de negocio
-   Causa raíz
-   Acciones correctivas
-   Medidas preventivas

Elemento fundamental para evitar recurrencias.

------------------------------------------------------------------------

## ▶️ Ejecución del ejemplo

Desde la carpeta del módulo:

``` bash
cd automatizacion_pipeline/incident_management
```

Configurar PYTHONPATH:

### Git Bash

``` bash
export PYTHONPATH=src
```

### PowerShell

``` powershell
set PYTHONPATH=src
```

Ejecutar simulación:

``` bash
python examples/simulate_incident.py
```

Salida esperada:

``` text
Handling pipeline_down incident...

Respuesta a incidente:
Tipo: pipeline_down
Severidad: CRITICAL
Resuelto: True
Pasos ejecutados:
check_airflow_scheduler
check_database_connectivity
restart_failed_services
verify_pipeline_recovery
```

------------------------------------------------------------------------

## 🧪 Ejecutar pruebas

``` bash
pytest tests -v
```

Resultado esperado:

``` text
4 passed
```

Las pruebas validan:

-   Manejo de incidentes desconocidos
-   Conversión correcta de tiempos
-   Escalamiento por severidad
-   Recuperación exitosa del pipeline

------------------------------------------------------------------------

## ✅ Verificación conceptual

### Diferencia entre incidentes críticos y no críticos

Un incidente requiere **respuesta inmediata** cuando:

-   Detiene pipelines críticos de producción.
-   Impacta decisiones de negocio en tiempo real.
-   Genera pérdida o corrupción de datos.
-   Afecta directamente a usuarios o clientes.
-   Bloquea procesos operativos clave.

Un incidente puede esperar cuando:

-   No impacta procesos críticos.
-   Existen mecanismos de contingencia activos.
-   El problema es limitado o local.
-   No hay pérdida de datos.
-   Puede resolverse en ventanas de mantenimiento.

La prioridad se define por:

-   Impacto en negocio
-   Sistemas afectados
-   Riesgo de pérdida de datos
-   Tiempo estimado de recuperación

------------------------------------------------------------------------

### Cuándo escalar un incidente

Un incidente debe escalarse cuando:

-   No se resuelve dentro del tiempo definido.
-   El impacto comienza a crecer.
-   Se requiere intervención fuera del equipo operativo.
-   Existe riesgo para el negocio.
-   Se necesitan recursos o decisiones superiores.

El runbook implementa:

-   Umbrales por severidad
-   Escalamiento progresivo
-   Notificaciones automáticas

Esto evita incidentes prolongados sin visibilidad.

------------------------------------------------------------------------

## 📈 Valor para el portafolio

Este módulo demuestra habilidades reales en:

-   Operación de pipelines
-   Gestión de incidentes
-   Automatización de recuperación
-   Testing de confiabilidad
-   Estrategias de escalamiento
-   Preparación para entornos productivos

Relevante para roles como:

-   Data Engineer
-   Analytics Engineer
-   Platform Engineer
-   Reliability Engineer

------------------------------------------------------------------------

## 🔮 Mejoras futuras posibles

Extensiones recomendadas:

-   Registro histórico de incidentes
-   Métricas MTTR / MTBF
-   Alertas Slack o email
-   Dashboard de incidentes
-   Integración con Airflow o Kafka
-   Simulación de fallos en producción

------------------------------------------------------------------------

## ✍️ Autor

**Fabián Díaz**\
Desarrollado como parte del repositorio **Kranio**, enfocado en
demostrar capacidades prácticas en ingeniería y operación de datos.
