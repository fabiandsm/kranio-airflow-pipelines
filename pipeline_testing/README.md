# Pipeline Testing – Validación y Testing de Datos

Este proyecto demuestra la implementación de una suite básica de tests unitarios para validar la lógica crítica de un pipeline de datos utilizando Python y pytest.

El objetivo es asegurar la calidad de los datos procesados y prevenir errores silenciosos antes de integrar el pipeline en flujos automatizados o entornos productivos.

---

## 📌 Objetivos de Aprendizaje

- Comprender la importancia del testing en pipelines de datos  
- Aplicar tests unitarios para validar lógica de negocio  
- Detectar errores comunes en procesos de transformación de datos  
- Preparar pipelines para su integración en CI/CD  

---

## 📂 Estructura del Proyecto

```
pipeline_testing/
│
├── pipeline.py          # Lógica principal del pipeline
├── test_pipeline.py     # Tests unitarios
├── requirements.txt     # Dependencias del proyecto
└── README.md
```

---

## ⚙️ Funcionalidad del Pipeline

El pipeline implementa una función que calcula el total de ventas por producto a partir de una lista de registros, simulando una etapa de transformación típica en un pipeline de datos.

---

## 🧪 Testing y Validación

Se implementaron tests unitarios utilizando pytest para validar:

- Cálculo correcto de totales por producto  
- Comportamiento del pipeline ante una lista de entrada vacía (edge case)  

Estos tests permiten detectar errores de lógica de manera temprana y asegurar la estabilidad del pipeline.

---

## ▶️ Ejecución de Tests

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar tests:

```bash
pytest -v
```

---

## ✅ Verificación
¿Por qué es importante testear pipelines de datos?
-   Testear pipelines de datos es clave para evitar errores silenciosos que puedan afectar métricas de negocio.  

¿Qué tipos de errores son más comunes en pipelines y cómo detectarlos con tests?
-   Los errores más comunes incluyen cálculos incorrectos, datos vacíos o inconsistentes y cambios involuntarios en la lógica del pipeline.  
    Estos problemas se detectan mediante tests unitarios y tests de borde que validan el comportamiento esperado del sistema bajo distintos escenarios.

---

## 🧠 Conclusión

La incorporación de testing en pipelines de datos mejora la confiabilidad, mantenibilidad y escalabilidad de los procesos, siendo una práctica esencial en proyectos de ingeniería y ciencia de datos.
