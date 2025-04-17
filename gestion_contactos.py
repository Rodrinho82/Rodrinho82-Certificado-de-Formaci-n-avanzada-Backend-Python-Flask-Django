import os
import re


class Contacto:  # Clase para representar un contacto
    def __init__(self, nombre, telefono, correo):
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo

    def __str__(self):
        return f"Nombre: {self.nombre}, Teléfono: {self.telefono}, Correo: {self.correo}"


class GestionContactos:  # Clase para gestionar los contactos
    def __init__(self, archivo='contactos.txt'):
        self.contactos = []
        self.archivo = archivo
        self.cargar_contactos()

    def agregar_contacto(self, nombre, telefono, correo):
        if not self.validar_correo(correo):
            print("❌ Error: El correo electrónico no tiene un formato válido.")
            return
        if not nombre.strip() or not telefono.strip() or not correo.strip():
            print("❌ Error: Todos los campos son obligatorios.")
            return
        if self.buscar_contacto(nombre):
            print("❌ Error: Ya existe un contacto con ese nombre.")
            return
        contacto = Contacto(nombre, telefono, correo)
        self.contactos.append(contacto)
        self.guardar_contactos()
        print("✅ Contacto agregado correctamente.")

    def mostrar_contactos(self):
        if not self.contactos:
            print("📭 No hay contactos para mostrar.")
        else:
            for contacto in self.contactos:
                print(contacto)

    def buscar_contacto(self, nombre):
        for contacto in self.contactos:
            if contacto.nombre.lower() == nombre.lower():
                return contacto
        return None

    def eliminar_contacto(self, nombre):
        contacto = self.buscar_contacto(nombre)
        if contacto:
            self.contactos.remove(contacto)
            self.guardar_contactos()
            print("🗑️ Contacto eliminado correctamente.")
        else:
            print("❌ Error: Contacto no encontrado.")

    def validar_correo(self, correo):
        return re.match(r"[^@]+@[^@]+\.[^@]+", correo)

    def guardar_contactos(self):
        try:
            with open(self.archivo, 'w') as f:
                for c in self.contactos:
                    f.write(f"{c.nombre},{c.telefono},{c.correo}\n")
        except IOError:
            print("❌ Error al guardar los contactos en el archivo.")

    def cargar_contactos(self):
        if not os.path.exists(self.archivo):
            return
        try:
            with open(self.archivo, 'r') as f:
                for linea in f:
                    partes = linea.strip().split(',')
                    if len(partes) == 3:
                        nombre, telefono, correo = partes
                        self.contactos.append(Contacto(nombre, telefono, correo))
        except IOError:
            print("❌ Error al cargar los contactos desde el archivo.")


def menu():  # Función principal del menú
    sistema = GestionContactos()

    while True:
        print("\n📒 Menú del Sistema de Gestión de Contactos")
        print("1. Agregar contacto")
        print("2. Mostrar todos los contactos")
        print("3. Buscar contacto por nombre")
        print("4. Eliminar contacto")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            nombre = input("Nombre: ")
            telefono = input("Teléfono: ")
            correo = input("Correo electrónico: ")
            sistema.agregar_contacto(nombre, telefono, correo)
        elif opcion == '2':
            sistema.mostrar_contactos()
        elif opcion == '3':
            nombre = input("Nombre del contacto a buscar: ")
            contacto = sistema.buscar_contacto(nombre)
            if contacto:
                print(contacto)
            else:
                print("❌ Contacto no encontrado.")
        elif opcion == '4':
            nombre = input("Nombre del contacto a eliminar: ")
            sistema.eliminar_contacto(nombre)
        elif opcion == '5':
            print("👋 ¡Hasta luego!, Gracias por usar nuestro gestor de contactos..¡")
            break
        else:
            print("❌ Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    menu()
