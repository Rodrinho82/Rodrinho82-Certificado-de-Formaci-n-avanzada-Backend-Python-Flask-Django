import mysql.connector
from mysql.connector import Error


class InventarioDB:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='admin',
                database='inventario'
            )
            self.cursor = self.conn.cursor()
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            exit()

    def agregar_producto(self, nombre, cantidad, precio, categoria):
        try:
            query = "INSERT INTO productos (nombre, cantidad, precio, categoria) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (nombre, cantidad, precio, categoria))
            self.conn.commit()
            print("✅ Producto agregado exitosamente.")
        except Error as e:
            print(f"Error al agregar producto: {e}")

    def mostrar_productos(self):
        try:
            self.cursor.execute("SELECT * FROM productos")
            productos = self.cursor.fetchall()
            if productos:
                for prod in productos:
                    print(
                        f"ID: {prod[0]}, Nombre: {prod[1]}, Cantidad: {prod[2]}, Precio: {prod[3]}, Categoría: {prod[4]}")
            else:
                print("📦 No hay productos en el inventario.")
        except Error as e:
            print(f"Error al mostrar productos: {e}")

    def buscar_productos(self, criterio, valor):
        try:
            query = f"SELECT * FROM productos WHERE {criterio} LIKE %s"
            self.cursor.execute(query, (f"%{valor}%",))
            resultados = self.cursor.fetchall()
            if resultados:
                for prod in resultados:
                    print(
                        f"ID: {prod[0]}, Nombre: {prod[1]}, Cantidad: {prod[2]}, Precio: {prod[3]}, Categoría: {prod[4]}")
            else:
                print("🔍 No se encontraron productos con ese criterio.")
        except Error as e:
            print(f"Error al buscar productos: {e}")

    def actualizar_producto(self, id, nombre, cantidad, precio, categoria):
        try:
            query = "UPDATE productos SET nombre=%s, cantidad=%s, precio=%s, categoria=%s WHERE id=%s"
            self.cursor.execute(query, (nombre, cantidad, precio, categoria, id))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print("✅ Producto actualizado.")
            else:
                print("⚠️ No se encontró un producto con ese ID.")
        except Error as e:
            print(f"Error al actualizar producto: {e}")

    def eliminar_producto(self, id):
        try:
            self.cursor.execute("DELETE FROM productos WHERE id=%s", (id,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print("🗑️ Producto eliminado.")
            else:
                print("⚠️ No se encontró un producto con ese ID.")
        except Error as e:
            print(f"Error al eliminar producto: {e}")

    def cerrar_conexion(self):
        self.cursor.close()
        self.conn.close()


def menu():
    db = InventarioDB()
    while True:
        print("\n--- Menú de Inventario ---")
        print("1. Agregar producto")
        print("2. Mostrar productos")
        print("3. Actualizar producto")
        print("4. Buscar producto")
        print("5. Eliminar producto")
        print("6. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            nombre = input("Nombre: ")
            cantidad = int(input("Cantidad: "))
            precio = float(input("Precio: "))
            categoria = input("Categoría: ")
            db.agregar_producto(nombre, cantidad, precio, categoria)

        elif opcion == '2':
            db.mostrar_productos()

        elif opcion == '3':
            id = int(input("ID del producto a actualizar: "))
            nombre = input("Nuevo nombre: ")
            cantidad = int(input("Nueva cantidad: "))
            precio = float(input("Nuevo precio: "))
            categoria = input("Nueva categoría: ")
            db.actualizar_producto(id, nombre, cantidad, precio, categoria)

        elif opcion == '4':
            print("Buscar por:")
            print("1. Nombre")
            print("2. Categoría")
            tipo = input("Selecciona: ")
            if tipo == '1':
                valor = input("Introduce el nombre a buscar: ")
                db.buscar_productos("nombre", valor)
            elif tipo == '2':
                valor = input("Introduce la categoría a buscar: ")
                db.buscar_productos("categoria", valor)
            else:
                print("❌ Opción no válida.")


        elif opcion == '5':
            id = int(input("ID del producto a eliminar: "))
            db.eliminar_producto(id)

        elif opcion == '6':
            db.cerrar_conexion()
            print("👋 Saliendo del sistema...")
            break
        else:
            print("❌ Opción no válida. Intenta nuevamente.")


if __name__ == "__main__":
    menu()
