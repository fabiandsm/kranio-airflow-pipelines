# Pipeline Avanzado — Best Practices en Airflow

## Descripción

Este DAG demuestra el uso de patrones avanzados en Apache Airflow para construir pipelines robustos, escalables y mantenibles.

Incluye buenas prácticas comunes en entornos productivos como:

- Branching dinámico
- TaskGroups
- Control de flujo
- Reintentos automáticos
- Organización modular del pipeline

El pipeline simula un flujo donde se valida la calidad de datos y se decide dinámicamente la ruta de procesamiento.

---

## Flujo del Pipeline

1. Inicio del pipeline.
2. Validación de calidad de datos.
3. Decisión automática de ruta según calidad.
4. Procesamiento rápido o completo.
5. Procesamiento pesado agrupado.
6. Unión de rutas.
7. Finalización del pipeline.

---

## Componentes Clave

### BranchPythonOperator
Permite elegir dinámicamente la ruta del pipeline según la calidad detectada.

### TaskGroup
Agrupa tareas complejas para mantener el DAG legible y organizado.

### Manejo de reintentos
El pipeline incluye retries automáticos para tolerancia a fallos.

---

## Buenas prácticas aplicadas

- DAG limpio y modular
- Separación lógica de tareas
- Uso de operadores especializados
- Flujo claro y escalable
- Preparado para producción

---

## Objetivo del ejercicio

Demostrar cómo construir pipelines complejos manteniendo claridad y escalabilidad.

Este patrón es típico en pipelines productivos de datos.

---

## DAG generado

`pipeline_avanzado_complejo`
