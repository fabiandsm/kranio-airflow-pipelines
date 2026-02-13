from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from datetime import datetime
import pandas as pd


# =========================
# Funciones de negocio
# =========================

def procesar_datos():
    print("Procesando datos de ventas...")
    return "Datos procesados"


def generar_reporte():
    print("Generando reporte ejecutivo...")
    return "Reporte generado"


# =========================
# Operador personalizado
# =========================

class ValidadorDatosOperator(BaseOperator):
    """
    Operador personalizado para validar calidad de datos
    """

    @apply_defaults
    def __init__(self, archivo_entrada, umbral_calidad=0.9, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.archivo_entrada = archivo_entrada
        self.umbral_calidad = umbral_calidad

    def execute(self, context):
        self.log.info(f"Validando archivo: {self.archivo_entrada}")

        # Leer archivo
        try:
            df = pd.read_csv(self.archivo_entrada)
        except Exception as e:
            raise Exception(f"Error leyendo archivo: {e}")

        total_registros = len(df)
        registros_completos = df.dropna().shape[0]

        if total_registros == 0:
            raise Exception("El archivo no contiene registros")

        calidad = registros_completos / total_registros

        self.log.info(f"Registros totales: {total_registros}")
        self.log.info(f"Registros completos: {registros_completos}")
        self.log.info(f"Calidad de datos: {calidad:.2%}")

        if calidad < self.umbral_calidad:
            raise Exception(
                f"Calidad insuficiente: {calidad:.2%} < {self.umbral_calidad:.2%}"
            )

        return {
            "registros_totales": total_registros,
            "registros_validos": registros_completos,
            "calidad": calidad
        }


# =========================
# Definición del DAG
# =========================

dag = DAG(
    dag_id="pipeline_con_sensores_y_operador_custom",
    description="Pipeline con sensor de archivos y validación de calidad",
    schedule_interval="@hourly",
    start_date=datetime(2024, 1, 1),
    catchup=False,
)


# =========================
# Tareas
# =========================

# Sensor que espera archivo
esperar_datos = FileSensor(
    task_id="esperar_archivo_datos",
    filepath="/tmp/datos_ventas.csv",
    poke_interval=60,
    timeout=3600,
    mode="poke",
    dag=dag,
)

# Validación de calidad
validar_datos = ValidadorDatosOperator(
    task_id="validar_datos_ventas",
    archivo_entrada="/tmp/datos_ventas.csv",
    umbral_calidad=0.95,
    dag=dag,
)

# Procesamiento
procesar = PythonOperator(
    task_id="procesar_datos_ventas",
    python_callable=procesar_datos,
    dag=dag,
)

# Generación de reporte
reporte = PythonOperator(
    task_id="generar_reporte",
    python_callable=generar_reporte,
    dag=dag,
)

# Limpieza
limpiar = BashOperator(
    task_id="limpiar_archivos",
    bash_command="rm -f /tmp/datos_ventas.csv",
    dag=dag,
)


# =========================
# Dependencias
# =========================

esperar_datos >> validar_datos >> procesar >> reporte >> limpiar
