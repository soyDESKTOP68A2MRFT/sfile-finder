import gi
import subprocess
import shutil

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Define el nombre del script de Bash
SCRIPT_PATH = "/home/joni/sfile/sfile"  # El script está en el PATH del sistema.

class BuscarArchivos:
    def __init__(self):
        # Cargar la interfaz desde el archivo Glade
        builder = Gtk.Builder()
        builder.add_from_file("/home/joni/sfile/sfile.glade")
        builder.connect_signals(self)
        
        # Obtener los widgets necesarios
        self.window = builder.get_object("main_window")
        self.entry_directorio = builder.get_object("entry_directorio")
        self.entry_palabra = builder.get_object("entry_palabra")
        self.textview_resultados = builder.get_object("textview_resultados")
        
        # Mostrar la ventana
        self.window.show_all()
    
    def on_btn_buscar_clicked(self, widget):
        # Obtener valores de los campos de texto
        directorio = self.entry_directorio.get_text().strip()
        palabra = self.entry_palabra.get_text().strip()
        
        if not directorio or not palabra:
            self.mostrar_resultado("Por favor, complete todos los campos.")
            return
        
        # Verificar si el script está en el PATH
        if not shutil.which(SCRIPT_PATH):
            self.mostrar_resultado("Error: No se encontró el script en el PATH.")
            return
        
        try:
            # Ejecutar el script de Bash
            resultado = subprocess.check_output(
                [SCRIPT_PATH, directorio, palabra],
                stderr=subprocess.STDOUT,
                text=True
            )
            self.mostrar_resultado(resultado)
        except subprocess.CalledProcessError as e:
            self.mostrar_resultado(f"Error al ejecutar el script:\n{e.output}")
        except Exception as e:
            self.mostrar_resultado(f"Error inesperado:\n{str(e)}")
    
    def mostrar_resultado(self, texto):
        # Mostrar el resultado en el TextView
        buffer = self.textview_resultados.get_buffer()
        buffer.set_text(texto)
    
    def on_main_window_destroy(self, widget):
        # Finalizar la aplicación cuando se cierre la ventana
        Gtk.main_quit()

if __name__ == "__main__":
    app = BuscarArchivos()
    Gtk.main()
