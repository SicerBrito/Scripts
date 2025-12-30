"""
Interfaz Gráfica para Herramienta de Excel
Requiere: pip install pywin32
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import win32com.client
import zipfile
import os
import re
import shutil
import tempfile
from pathlib import Path


class ExcelToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Herramienta de Excel - Reparar y Desproteger")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
        # Variables
        self.archivo_seleccionado = tk.StringVar()
        self.procesando = False
        
        # Colores modernos
        self.color_primario = "#2563eb"  # Azul
        self.color_secundario = "#64748b"  # Gris
        self.color_exito = "#10b981"  # Verde
        self.color_error = "#ef4444"  # Rojo
        self.color_warning = "#f59e0b"  # Naranja
        self.color_fondo = "#f8fafc"  # Gris claro
        self.color_texto = "#1e293b"  # Gris oscuro
        
        self.root.configure(bg=self.color_fondo)
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.color_primario, height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🔧 Herramienta de Excel",
            font=("Segoe UI", 24, "bold"),
            bg=self.color_primario,
            fg="white"
        ).pack(pady=20)
        
        # Container principal
        main_container = tk.Frame(self.root, bg=self.color_fondo)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Sección: Seleccionar archivo
        self.crear_seccion_archivo(main_container)
        
        # Sección: Opciones
        self.crear_seccion_opciones(main_container)
        
        # Sección: Botones de acción
        self.crear_seccion_botones(main_container)
        
        # Sección: Log/Consola
        self.crear_seccion_log(main_container)
        
        # Barra de progreso
        self.crear_barra_progreso(main_container)
    
    def crear_seccion_archivo(self, parent):
        """Sección para seleccionar archivo"""
        frame = tk.LabelFrame(
            parent,
            text="  📁 Archivo de Excel  ",
            font=("Segoe UI", 12, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto,
            padx=15,
            pady=15
        )
        frame.pack(fill=tk.X, pady=(0, 15))
        
        # Entry para mostrar ruta
        entry_frame = tk.Frame(frame, bg=self.color_fondo)
        entry_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.archivo_entry = tk.Entry(
            entry_frame,
            textvariable=self.archivo_seleccionado,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            bg="white",
            fg=self.color_texto,
            state="readonly"
        )
        self.archivo_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=8, padx=(0, 10))
        
        # Botón seleccionar
        self.btn_seleccionar = tk.Button(
            entry_frame,
            text="Seleccionar Archivo",
            command=self.seleccionar_archivo,
            font=("Segoe UI", 10, "bold"),
            bg=self.color_primario,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8
        )
        self.btn_seleccionar.pack(side=tk.RIGHT)
        self.btn_seleccionar.bind("<Enter>", lambda e: self.btn_seleccionar.config(bg="#1d4ed8"))
        self.btn_seleccionar.bind("<Leave>", lambda e: self.btn_seleccionar.config(bg=self.color_primario))
    
    def crear_seccion_opciones(self, parent):
        """Sección de opciones del proceso"""
        frame = tk.LabelFrame(
            parent,
            text="  ⚙️ Opciones  ",
            font=("Segoe UI", 12, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto,
            padx=15,
            pady=15
        )
        frame.pack(fill=tk.X, pady=(0, 15))
        
        self.var_diagnostico = tk.BooleanVar(value=True)
        self.var_reparacion = tk.BooleanVar(value=True)
        self.var_desproteccion = tk.BooleanVar(value=True)
        
        tk.Checkbutton(
            frame,
            text="🔍 Realizar diagnóstico inicial",
            variable=self.var_diagnostico,
            font=("Segoe UI", 10),
            bg=self.color_fondo,
            fg=self.color_texto,
            selectcolor="white",
            activebackground=self.color_fondo,
            cursor="hand2"
        ).pack(anchor=tk.W, pady=3)
        
        tk.Checkbutton(
            frame,
            text="🔧 Reparar archivo (si es necesario)",
            variable=self.var_reparacion,
            font=("Segoe UI", 10),
            bg=self.color_fondo,
            fg=self.color_texto,
            selectcolor="white",
            activebackground=self.color_fondo,
            cursor="hand2"
        ).pack(anchor=tk.W, pady=3)
        
        tk.Checkbutton(
            frame,
            text="🔓 Desproteger hojas",
            variable=self.var_desproteccion,
            font=("Segoe UI", 10),
            bg=self.color_fondo,
            fg=self.color_texto,
            selectcolor="white",
            activebackground=self.color_fondo,
            cursor="hand2"
        ).pack(anchor=tk.W, pady=3)
    
    def crear_seccion_botones(self, parent):
        """Botones de acción principal"""
        frame = tk.Frame(parent, bg=self.color_fondo)
        frame.pack(fill=tk.X, pady=(0, 15))
        
        # Botón procesar
        self.btn_procesar = tk.Button(
            frame,
            text="🚀 Iniciar Proceso",
            command=self.iniciar_proceso,
            font=("Segoe UI", 12, "bold"),
            bg=self.color_exito,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=30,
            pady=12
        )
        self.btn_procesar.pack(side=tk.LEFT, padx=(0, 10))
        self.btn_procesar.bind("<Enter>", lambda e: self.btn_procesar.config(bg="#059669"))
        self.btn_procesar.bind("<Leave>", lambda e: self.btn_procesar.config(bg=self.color_exito))
        
        # Botón solo diagnóstico
        self.btn_diagnostico = tk.Button(
            frame,
            text="🔍 Solo Diagnóstico",
            command=self.solo_diagnostico,
            font=("Segoe UI", 12, "bold"),
            bg=self.color_warning,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=30,
            pady=12
        )
        self.btn_diagnostico.pack(side=tk.LEFT, padx=(0, 10))
        self.btn_diagnostico.bind("<Enter>", lambda e: self.btn_diagnostico.config(bg="#d97706"))
        self.btn_diagnostico.bind("<Leave>", lambda e: self.btn_diagnostico.config(bg=self.color_warning))
        
        # Botón limpiar
        btn_limpiar = tk.Button(
            frame,
            text="🗑️ Limpiar",
            command=self.limpiar_log,
            font=("Segoe UI", 11),
            bg=self.color_secundario,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=12
        )
        btn_limpiar.pack(side=tk.RIGHT)
        btn_limpiar.bind("<Enter>", lambda e: btn_limpiar.config(bg="#475569"))
        btn_limpiar.bind("<Leave>", lambda e: btn_limpiar.config(bg=self.color_secundario))
    
    def crear_seccion_log(self, parent):
        """Área de log/consola"""
        frame = tk.LabelFrame(
            parent,
            text="  📋 Registro de Actividad  ",
            font=("Segoe UI", 12, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto,
            padx=10,
            pady=10
        )
        frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(
            frame,
            font=("Consolas", 9),
            bg="#1e293b",
            fg="#e2e8f0",
            relief=tk.FLAT,
            wrap=tk.WORD,
            height=15
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)
    
    def crear_barra_progreso(self, parent):
        """Barra de progreso"""
        self.progress = ttk.Progressbar(
            parent,
            mode='indeterminate',
            length=760
        )
        self.progress.pack(fill=tk.X)
    
    def seleccionar_archivo(self):
        """Abre diálogo para seleccionar archivo"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[
                ("Archivos Excel", "*.xlsx *.xlsm *.xls"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if archivo:
            self.archivo_seleccionado.set(archivo)
            self.log(f"✅ Archivo seleccionado: {Path(archivo).name}", "exito")
    
    def log(self, mensaje, tipo="info"):
        """Agrega mensaje al log con colores"""
        self.log_text.config(state=tk.NORMAL)
        
        # Colores según tipo
        colores = {
            "info": "#e2e8f0",
            "exito": "#10b981",
            "error": "#ef4444",
            "warning": "#f59e0b",
            "header": "#60a5fa"
        }
        
        color = colores.get(tipo, colores["info"])
        
        # Crear tag si no existe
        if tipo not in self.log_text.tag_names():
            self.log_text.tag_config(tipo, foreground=color)
        
        self.log_text.insert(tk.END, mensaje + "\n", tipo)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
    
    def limpiar_log(self):
        """Limpia el área de log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def deshabilitar_botones(self):
        """Deshabilita botones durante el proceso"""
        self.btn_procesar.config(state=tk.DISABLED)
        self.btn_diagnostico.config(state=tk.DISABLED)
        self.btn_seleccionar.config(state=tk.DISABLED)
        self.progress.start()
    
    def habilitar_botones(self):
        """Habilita botones después del proceso"""
        self.btn_procesar.config(state=tk.NORMAL)
        self.btn_diagnostico.config(state=tk.NORMAL)
        self.btn_seleccionar.config(state=tk.NORMAL)
        self.progress.stop()
    
    def solo_diagnostico(self):
        """Ejecuta solo diagnóstico"""
        if not self.archivo_seleccionado.get():
            messagebox.showwarning("Advertencia", "Por favor selecciona un archivo primero")
            return
        
        def ejecutar():
            self.deshabilitar_botones()
            self.limpiar_log()
            
            try:
                toolkit = ExcelToolkit(self.archivo_seleccionado.get(), self.log)
                toolkit.diagnosticar()
                
                self.log("\n✅ Diagnóstico completado", "exito")
                messagebox.showinfo("Éxito", "Diagnóstico completado correctamente")
            except Exception as e:
                self.log(f"\n❌ Error: {str(e)}", "error")
                messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")
            finally:
                self.habilitar_botones()
        
        threading.Thread(target=ejecutar, daemon=True).start()
    
    def iniciar_proceso(self):
        """Inicia el proceso completo"""
        if not self.archivo_seleccionado.get():
            messagebox.showwarning("Advertencia", "Por favor selecciona un archivo primero")
            return
        
        if not (self.var_diagnostico.get() or self.var_reparacion.get() or self.var_desproteccion.get()):
            messagebox.showwarning("Advertencia", "Selecciona al menos una opción")
            return
        
        def ejecutar():
            self.deshabilitar_botones()
            self.limpiar_log()
            
            try:
                toolkit = ExcelToolkit(self.archivo_seleccionado.get(), self.log)
                
                opciones = {
                    'diagnostico': self.var_diagnostico.get(),
                    'reparacion': self.var_reparacion.get(),
                    'desproteccion': self.var_desproteccion.get()
                }
                
                toolkit.proceso_completo(opciones)
                
                self.log("\n" + "=" * 70, "header")
                self.log("✅ PROCESO COMPLETADO EXITOSAMENTE", "exito")
                self.log("=" * 70, "header")
                
                messagebox.showinfo("Éxito", "¡Proceso completado exitosamente!")
            except Exception as e:
                self.log(f"\n❌ Error: {str(e)}", "error")
                messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")
            finally:
                self.habilitar_botones()
        
        threading.Thread(target=ejecutar, daemon=True).start()


class ExcelToolkit:
    """Clase de backend (misma lógica del script anterior)"""
    
    def __init__(self, archivo_excel, log_callback):
        self.archivo_original = Path(archivo_excel).resolve()
        self.archivo_reparado = None
        self.archivo_desprotegido = None
        self.excel = None
        self.wb = None
        self.log = log_callback
        
        if not self.archivo_original.exists():
            raise FileNotFoundError(f"El archivo no existe: {archivo_excel}")
    
    def _iniciar_excel(self):
        if not self.excel:
            self.excel = win32com.client.Dispatch("Excel.Application")
            self.excel.Visible = False
            self.excel.DisplayAlerts = False
    
    def _cerrar_excel(self):
        try:
            if self.wb: self.wb.Close(SaveChanges=False)
            if self.excel: self.excel.Quit()
        except: pass
        finally:
            self.excel = None
            self.wb = None
    
    def diagnosticar(self, archivo=None):
        archivo = archivo or self.archivo_original
        
        self.log("\n" + "=" * 70, "header")
        self.log("🔍 DIAGNÓSTICO", "header")
        self.log("=" * 70, "header")
        self.log(f"Archivo: {archivo.name}", "info")
        
        try:
            self._iniciar_excel()
            self.wb = self.excel.Workbooks.Open(str(archivo))
            
            self.log(f"\n📊 Total de hojas: {self.wb.Worksheets.Count}", "info")
            
            hojas_protegidas = 0
            
            for i in range(1, self.wb.Worksheets.Count + 1):
                sheet = self.wb.Worksheets(i)
                nombre = sheet.Name
                visible = "Visible" if sheet.Visible == -1 else "Oculta"
                
                if sheet.ProtectContents:
                    estado = "🔒 PROTEGIDA"
                    tipo = "warning"
                    hojas_protegidas += 1
                else:
                    estado = "✅ LIBRE"
                    tipo = "exito"
                
                self.log(f"   {i:2}. {estado:15} | {nombre:30} | {visible}", tipo)
            
            self.log(f"\n📊 Resumen:", "info")
            self.log(f"   Hojas protegidas: {hojas_protegidas}", "warning" if hojas_protegidas > 0 else "exito")
            self.log(f"   Hojas libres: {self.wb.Worksheets.Count - hojas_protegidas}", "exito")
            
            return hojas_protegidas > 0
            
        except Exception as e:
            self.log(f"❌ Error: {e}", "error")
            return False
        finally:
            self._cerrar_excel()
    
    def reparar(self):
        self.log("\n" + "=" * 70, "header")
        self.log("🔧 REPARACIÓN", "header")
        self.log("=" * 70, "header")
        
        backup = str(self.archivo_original.with_suffix('')) + '.backup' + self.archivo_original.suffix
        shutil.copy(str(self.archivo_original), backup)
        self.log(f"✅ Backup creado: {Path(backup).name}", "exito")
        
        try:
            self._iniciar_excel()
            self.log("📂 Abriendo y reparando archivo...", "info")
            
            self.wb = self.excel.Workbooks.Open(
                str(self.archivo_original),
                UpdateLinks=0,
                ReadOnly=False,
                CorruptLoad=1
            )
            
            self.log(f"✅ Archivo reparado ({self.wb.Worksheets.Count} hojas)", "exito")
            
            self.archivo_reparado = self.archivo_original.with_name(
                self.archivo_original.stem + '_REPARADO' + self.archivo_original.suffix
            )
            
            self.log("💾 Guardando archivo reparado...", "info")
            
            if self.archivo_original.suffix.lower() == '.xlsm':
                self.wb.SaveAs(str(self.archivo_reparado), FileFormat=52)
            else:
                self.wb.SaveAs(str(self.archivo_reparado), FileFormat=51)
            
            self.log(f"✅ Guardado: {self.archivo_reparado.name}", "exito")
            return True
            
        except Exception as e:
            self.log(f"❌ Error: {e}", "error")
            return False
        finally:
            self._cerrar_excel()
    
    def desproteger_xml(self, archivo_entrada):
        self.log("\n" + "=" * 70, "header")
        self.log("🔓 DESPROTECCIÓN", "header")
        self.log("=" * 70, "header")
        
        temp_dir = tempfile.mkdtemp()
        
        try:
            self.log("📦 Extrayendo contenido...", "info")
            
            with zipfile.ZipFile(str(archivo_entrada), 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            hojas_modificadas = 0
            
            worksheets_dir = os.path.join(temp_dir, 'xl', 'worksheets')
            if os.path.exists(worksheets_dir):
                self.log("\n📄 Procesando hojas...", "info")
                
                for filename in sorted(os.listdir(worksheets_dir)):
                    if filename.endswith('.xml'):
                        filepath = os.path.join(worksheets_dir, filename)
                        
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        original = content
                        content = re.sub(r'<sheetProtection[^>]*/?>', '', content)
                        content = re.sub(r'<sheetProtection[^>]*>.*?</sheetProtection>', '', content, flags=re.DOTALL)
                        content = re.sub(r'<protectedRanges[^>]*>.*?</protectedRanges>', '', content, flags=re.DOTALL)
                        
                        if content != original:
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(content)
                            self.log(f"   ✅ {filename} desprotegida", "exito")
                            hojas_modificadas += 1
            
            workbook_file = os.path.join(temp_dir, 'xl', 'workbook.xml')
            if os.path.exists(workbook_file):
                with open(workbook_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original = content
                content = re.sub(r'<workbookProtection[^>]*/?>', '', content)
                content = re.sub(r'<workbookProtection[^>]*>.*?</workbookProtection>', '', content, flags=re.DOTALL)
                
                if content != original:
                    with open(workbook_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.log("✅ Libro desprotegido", "exito")
                    hojas_modificadas += 1
            
            self.log(f"\n✅ Elementos desprotegidos: {hojas_modificadas}", "exito")
            
            self.archivo_desprotegido = archivo_entrada.with_name(
                archivo_entrada.stem.replace('_REPARADO', '') + '_FINAL' + archivo_entrada.suffix
            )
            
            self.log("📦 Reempaquetando...", "info")
            
            with zipfile.ZipFile(str(self.archivo_desprotegido), 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zipf.write(file_path, arcname)
            
            self.log(f"✅ Archivo final: {self.archivo_desprotegido.name}", "exito")
            return True
            
        except Exception as e:
            self.log(f"❌ Error: {e}", "error")
            return False
        finally:
            try:
                shutil.rmtree(temp_dir)
            except: pass
    
    def proceso_completo(self, opciones):
        self.log("=" * 70, "header")
        self.log("🚀 INICIANDO PROCESO COMPLETO", "header")
        self.log("=" * 70, "header")
        
        archivo_para_desproteger = self.archivo_original
        
        if opciones['diagnostico']:
            self.diagnosticar()
        
        if opciones['reparacion']:
            if self.reparar():
                archivo_para_desproteger = self.archivo_reparado
        
        if opciones['desproteccion']:
            if self.desproteger_xml(archivo_para_desproteger):
                if opciones['diagnostico']:
                    self.diagnosticar(self.archivo_desprotegido)


def main():
    root = tk.Tk()
    app = ExcelToolGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()