# Pipeline con Monitoreo y Observabilidad

## Descripción

Este DAG demuestra cómo implementar monitoreo completo en un pipeline de datos usando:

- Métricas operacionales
- Logging estructurado
- Callbacks de éxito y falla
- Métricas de duración
- Control de SLA
- Medición de throughput y calidad

El objetivo es mostrar cómo construir pipelines observables y preparados para producción.

---

## Flujo del Pipeline

1. Extracción de datos
2. Transformación
3. Carga de datos
4. Callbacks de éxito/falla
5. Medición de métricas operacionales

---

## Métricas monitoreadas

El pipeline reporta métricas como:

- Registros procesados
- Duración de tareas
- Throughput de carga
- Calidad de datos
- Errores por etapa
- Duración total del DAG
- Violaciones SLA

Estas métricas permiten detectar degradaciones antes de impactar usuarios.

---

## Callbacks implementados

### DAG Success Callback
Registra duración y éxito del pipeline.

### DAG Failure Callback
Registra fallos del pipeline.

### SLA Miss Callback
Detecta retrasos en ejecución.

---

## Observabilidad en pipelines

La observabilidad permite:

- Detectar errores rápidamente
- Monitorear rendimiento
- Prevenir impactos en producción
- Facilitar debugging
- Mejorar estabilidad del sistema

---

## Verificación Conceptual

### Diferencia de métricas: Pipeline vs aplicación web

**Pipeline de datos**
- Registros procesados
- Duración de tareas
- Throughput
- Calidad de datos
- Fallos por etapa

**Aplicación web**
- Latencia de respuesta
- Usuarios activos
- Tasa de errores HTTP
- Disponibilidad del servicio

---

### Escalar alertas de warning a critical

Una alerta pasa de warning a critical cuando:

- Impacta a usuarios o sistemas dependientes
- El pipeline deja de entregar datos
- Se incumplen SLA repetidamente
- Hay pérdida o corrupción de datos
- El throughput cae bajo niveles mínimos aceptables

---

## Objetivo del ejercicio

Demostrar cómo construir pipelines listos para producción con monitoreo y métricas integradas.
