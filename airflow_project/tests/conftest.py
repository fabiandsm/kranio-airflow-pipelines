import sys
import os
from pathlib import Path
from unittest.mock import MagicMock

# ======================================================
# Asegurar root del proyecto en PYTHONPATH
# ======================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

# ======================================================
# FIX GLOBAL WINDOWS (Airflow importa fcntl)
# ======================================================
sys.modules["fcntl"] = MagicMock()

# ======================================================
# Configuración Airflow ANTES de importar airflow
# ======================================================
AIRFLOW_HOME = PROJECT_ROOT / "airflow_project"

os.environ["AIRFLOW_HOME"] = str(AIRFLOW_HOME)
os.environ["AIRFLOW__DATABASE__SQL_ALCHEMY_CONN"] = (
    "sqlite:////D:/Datos_Escritorio/Kranio/GitHub/Kranio/airflow_project/airflow_test.db"
)
os.environ["AIRFLOW__CORE__LOAD_EXAMPLES"] = "False"
os.environ["AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION"] = "True"

