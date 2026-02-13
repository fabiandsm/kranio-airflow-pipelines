# =============================================================================
# Pipeline básico con manejo de errores
# Objetivo: Demostrar pipeline end-to-end, manejo de estado y debugging
# =============================================================================

pipeline_simple = {
    'paso_1': 'Capturar datos de API',
    'paso_2': 'Validar y limpiar datos',
    'paso_3': 'Guardar en base de datos'
}


def ejecutar_pipeline_con_errores(pipeline):
    estado_pipeline = {}

    for paso, descripcion in pipeline.items():
        try:
            print(f"[INFO] Ejecutando {paso}: {descripcion}")

            # Simulación de ejecución
            if paso == 'paso_2':
                raise ValueError("Error de validación: datos inconsistentes")

            estado_pipeline[paso] = "OK"
            print(f"[SUCCESS] {paso} completado correctamente")

        except ValueError as e:
            estado_pipeline[paso] = f"ERROR: {str(e)}"
            print(f"[ERROR] Falló {paso} → {e}")
            print("[INFO] Deteniendo pipeline para evitar propagación de errores")
            break

    return estado_pipeline


if __name__ == "__main__":
    resultado = ejecutar_pipeline_con_errores(pipeline_simple)
    print("\nEstado final del pipeline:")
    print(resultado)

