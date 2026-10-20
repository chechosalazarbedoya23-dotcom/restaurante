import mysql.connector
import pandas as pd

# Conexión a la base de datos MySQL Workbench
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="tu_password",  # ⚠️ CAMBIA POR TU CONTRASEÑA REAL DE MYSQL
        database="restaurante_db",
        port=3306
    )

def mostrar_mesas():
    print("\n--- LISTADO DE MESAS DISPONIBLES ---")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, num_mesa, capacidad, ubicacion FROM Mesa")
        mesas = cursor.fetchall()
        
        if not mesas:
            print("No hay mesas registradas en la base de datos.")
        else:
            print(f"{'ID':<5} | {'N° Mesa':<10} | {'Capacidad':<10} | {'Ubicación':<15}")
            print("-" * 50)
            for mesa in mesas:
                print(f"{mesa[0]:<5} | {mesa[1]:<10} | {mesa[2]:<10} | {mesa[3]:<15}")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error al obtener mesas: {e}")

def crear_usuario():
    print("\n--- REGISTRAR NUEVO USUARIO ---")
    nombre = input("Ingrese nombre completo: ")
    documento = input("Ingrese número de documento: ")
    telefono = input("Ingrese teléfono: ")
    otro_contacto = input("Ingrese otro contacto (opcional): ")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Usuario (nombre, documento, telefono, otro_contacto) VALUES (%s, %s, %s, %s)",
            (nombre, documento, telefono, otro_contacto)
        )
        conn.commit()
        print("\n¡Usuario registrado exitosamente en la base de datos!")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"\nError al registrar usuario: {e}")

def crear_reserva():
    print("\n--- CREAR NUEVA RESERVA ---")
    documento = input("Ingrese el documento del usuario: ")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nombre FROM Usuario WHERE documento = %s", (documento,))
        user = cursor.fetchone()

        if not user:
            print("\nError: El documento no existe. Registre al usuario primero.")
            cursor.close()
            conn.close()
            return

        print(f"Cliente encontrado: {user[1]}")
        mostrar_mesas()
        
        mesa_id = input("\nIngrese el ID de la mesa a reservar: ")
        fecha_hora = input("Ingrese fecha y hora (YYYY-MM-DD HH:MM): ")
        comensales = input("Ingrese número de comensales: ")
        observaciones = input("Observaciones (opcional): ")

        cursor.execute(
            "INSERT INTO Reserva (fecha_hora, comensales, observaciones, usuario_id, mesa_id) VALUES (%s, %s, %s, %s, %s)",
            (fecha_hora, comensales, observaciones, user[0], mesa_id)
        )
        conn.commit()
        print("\n¡Reserva realizada y guardada con éxito!")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"\nError al crear la reserva: {e}")

def exportar_excel():
    print("\n--- EXPORTAR RESERVAS A EXCEL ---")
    try:
        conn = get_db_connection()
        query = """
            SELECT r.id, u.nombre AS cliente, u.documento, r.fecha_hora, r.comensales, r.mesa_id, r.observaciones 
            FROM Reserva r 
            JOIN Usuario u ON r.usuario_id = u.id
        """
        df = pd.read_sql(query, conn)
        conn.close()

        filename = "reservas_reporte.xlsx"
        df.to_excel(filename, index=False)
        print(f"\n¡Reporte exportado con éxito como '{filename}'!")
    except Exception as e:
        print(f"\nError al exportar a Excel: {e}")

def menu_principal():
    while True:
        print("\n" + "="*40)
        print("  SISTEMA DE RESERVAS DE RESTAURANTE  ")
        print("="*40)
        print("1. Ver Mesas")
        print("2. Registrar Usuario")
        print("3. Crear Reserva")
        print("4. Exportar Reservas a Excel")
        print("5. Salir")
        
        opcion = input("\nSeleccione una opción (1-5): ")

        if opcion == "1":
            mostrar_mesas()
        elif opcion == "2":
            crear_usuario()
        elif opcion == "3":
            crear_reserva()
        elif opcion == "4":
            exportar_excel()
        elif opcion == "5":
            print("\n¡Saliendo del sistema! Hasta luego.")
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu_principal()