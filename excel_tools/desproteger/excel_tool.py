"""
Herramienta Unificada de Excel - Reparar, Desproteger y Diagnosticar
Requiere: pip install pywin32

Uso:
    python excel_tool.py "archivo.xlsm"
    python excel_tool.py "archivo.xlsm" --solo-diagnostico
    python excel_tool.py "archivo.xlsm" --skip-reparacion
"""

import win32com.client
import zipfile
import os
import re
import sys
import shutil
import tempfile
from pathlib import Path


class ExcelToolkit:
    """Clase principal para todas las operaciones de Excel"""
    
    def __init__(self, archivo_excel):
        self.archivo_original = Path(archivo_excel).resolve()
        self.archivo_reparado = None
        self.archivo_desprotegido = None
        self.excel = None
        self.wb = None
        
        if not self.archivo_original.exists():
            raise FileNotFoundError(f"El archivo no existe: {archivo_excel}")
    
    def _iniciar_excel(self):
        """Inicializa Excel COM"""
        if not self.excel:
            self.excel = win32com.client.Dispatch("Excel.Application")
            self.excel.Visible = False
            self.excel.DisplayAlerts = False
    
    def _cerrar_excel(self):
        """Cierra Excel limpiamente"""
        try:
            if self.wb:
                self.wb.Close(SaveChanges=False)
            if self.excel:
                self.excel.Quit()
        except:
            pass
        finally:
            self.excel = None
            self.wb = None
    
    def diagnosticar(self, archivo=None):
        """Paso 1: Diagnostica el estado de protección"""
        
        archivo = archivo or self.archivo_original
        
        print("\n" + "=" * 70)
        print("🔍 PASO 1: DIAGNÓSTICO")
        print("=" * 70)
        print(f"\nArchivo: {archivo.name}")
        
        try:
            self._iniciar_excel()
            self.wb = self.excel.Workbooks.Open(str(archivo))
            
            print(f"\n📊 Total de hojas: {self.wb.Worksheets.Count}")
            
            hojas_protegidas = []
            hojas_libres = []
            
            for i in range(1, self.wb.Worksheets.Count + 1):
                sheet = self.wb.Worksheets(i)
                nombre = sheet.Name
                visible = "Visible" if sheet.Visible == -1 else "Oculta"
                
                if sheet.ProtectContents:
                    estado = "🔒 PROTEGIDA"
                    hojas_protegidas.append(nombre)
                else:
                    estado = "✅ LIBRE"
                    hojas_libres.append(nombre)
                
                print(f"   {i:2}. {estado:15} | {nombre:30} | {visible}")
            
            print(f"\n📊 Resumen:")
            print(f"   Hojas protegidas: {len(hojas_protegidas)}")
            print(f"   Hojas libres:     {len(hojas_libres)}")
            
            if self.wb.ProtectStructure:
                print(f"   🔒 Libro con estructura protegida")
            
            return len(hojas_protegidas) > 0
            
        except Exception as e:
            print(f"\n❌ Error en diagnóstico: {e}")
            return False
            
        finally:
            self._cerrar_excel()
    
    def reparar(self):
        """Paso 2: Repara el archivo"""
        
        print("\n" + "=" * 70)
        print("🔧 PASO 2: REPARACIÓN")
        print("=" * 70)
        
        # Crear backup
        backup = str(self.archivo_original.with_suffix('')) + '.original.backup' + self.archivo_original.suffix
        shutil.copy(str(self.archivo_original), backup)
        print(f"✅ Backup creado: {Path(backup).name}")
        
        try:
            self._iniciar_excel()
            
            print("\n📂 Abriendo y reparando archivo...")
            
            # Intentar reparación
            self.wb = self.excel.Workbooks.Open(
                str(self.archivo_original),
                UpdateLinks=0,
                ReadOnly=False,
                CorruptLoad=1  # xlRepairFile
            )
            
            print(f"✅ Archivo reparado ({self.wb.Worksheets.Count} hojas)")
            
            # Guardar archivo reparado
            self.archivo_reparado = self.archivo_original.with_name(
                self.archivo_original.stem + '_REPARADO' + self.archivo_original.suffix
            )
            
            print(f"\n💾 Guardando archivo reparado...")
            
            if self.archivo_original.suffix.lower() == '.xlsm':
                self.wb.SaveAs(str(self.archivo_reparado), FileFormat=52)
            else:
                self.wb.SaveAs(str(self.archivo_reparado), FileFormat=51)
            
            print(f"✅ Guardado como: {self.archivo_reparado.name}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error en reparación: {e}")
            return False
            
        finally:
            self._cerrar_excel()
    
    def desproteger_xml(self, archivo_entrada):
        """Paso 3: Desprotege mediante modificación XML"""
        
        print("\n" + "=" * 70)
        print("🔓 PASO 3: DESPROTECCIÓN")
        print("=" * 70)
        
        temp_dir = tempfile.mkdtemp()
        
        try:
            print("\n📦 Extrayendo contenido del Excel...")
            
            with zipfile.ZipFile(str(archivo_entrada), 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            hojas_modificadas = 0
            
            # Desproteger hojas de trabajo
            worksheets_dir = os.path.join(temp_dir, 'xl', 'worksheets')
            if os.path.exists(worksheets_dir):
                print("\n📄 Procesando hojas de trabajo...")
                
                for filename in sorted(os.listdir(worksheets_dir)):
                    if filename.endswith('.xml'):
                        filepath = os.path.join(worksheets_dir, filename)
                        
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        original_content = content
                        
                        # Remover protecciones
                        content = re.sub(r'<sheetProtection[^>]*/?>', '', content)
                        content = re.sub(r'<sheetProtection[^>]*>.*?</sheetProtection>', '', content, flags=re.DOTALL)
                        content = re.sub(r'<protectedRanges[^>]*>.*?</protectedRanges>', '', content, flags=re.DOTALL)
                        
                        if content != original_content:
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(content)
                            print(f"   ✅ {filename} - Desprotegida")
                            hojas_modificadas += 1
                        else:
                            print(f"   ℹ️  {filename} - Sin protección")
            
            # Desproteger workbook
            workbook_file = os.path.join(temp_dir, 'xl', 'workbook.xml')
            if os.path.exists(workbook_file):
                with open(workbook_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                content = re.sub(r'<workbookProtection[^>]*/?>', '', content)
                content = re.sub(r'<workbookProtection[^>]*>.*?</workbookProtection>', '', content, flags=re.DOTALL)
                content = re.sub(r'<fileSharing[^>]*/?>', '', content)
                
                if content != original_content:
                    with open(workbook_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print("\n📘 Protección del libro removida")
                    hojas_modificadas += 1
            
            print(f"\n✅ Total de elementos desprotegidos: {hojas_modificadas}")
            
            # Reempaquetar
            self.archivo_desprotegido = archivo_entrada.with_name(
                archivo_entrada.stem.replace('_REPARADO', '') + '_FINAL' + archivo_entrada.suffix
            )
            
            print(f"\n📦 Reempaquetando archivo...")
            
            with zipfile.ZipFile(str(self.archivo_desprotegido), 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zipf.write(file_path, arcname)
            
            print(f"✅ Archivo final guardado: {self.archivo_desprotegido.name}")
            
            return True
            
        except zipfile.BadZipFile:
            print("\n❌ Error: El archivo no es un ZIP válido")
            return False
            
        except Exception as e:
            print(f"\n❌ Error en desprotección: {e}")
            return False
            
        finally:
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
    
    def proceso_completo(self, skip_reparacion=False):
        """Ejecuta el proceso completo"""
        
        print("\n" + "=" * 70)
        print("🚀 PROCESO COMPLETO DE REPARACIÓN Y DESPROTECCIÓN")
        print("=" * 70)
        print(f"\nArchivo de entrada: {self.archivo_original.name}")
        
        # Paso 1: Diagnóstico inicial
        tiene_proteccion = self.diagnosticar()
        
        if not tiene_proteccion and not skip_reparacion:
            print("\n✅ El archivo no tiene protección. ¿Deseas continuar con reparación? (s/n): ", end='')
            respuesta = input().lower().strip()
            if respuesta != 's':
                print("\n✅ Proceso cancelado por el usuario")
                return
        
        # Paso 2: Reparación (opcional)
        archivo_para_desproteger = self.archivo_original
        
        if not skip_reparacion:
            if self.reparar():
                archivo_para_desproteger = self.archivo_reparado
            else:
                print("\n⚠️  La reparación falló. Intentando desproteger el archivo original...")
        else:
            print("\n⏭️  Reparación omitida")
        
        # Paso 3: Desprotección
        if self.desproteger_xml(archivo_para_desproteger):
            # Paso 4: Diagnóstico final
            print("\n" + "=" * 70)
            print("🔍 VERIFICACIÓN FINAL")
            print("=" * 70)
            self.diagnosticar(self.archivo_desprotegido)
            
            print("\n" + "=" * 70)
            print("✅ PROCESO COMPLETADO EXITOSAMENTE")
            print("=" * 70)
            print(f"\n📁 Archivo final: {self.archivo_desprotegido.name}")
            print(f"📁 Ubicación: {self.archivo_desprotegido.parent}")
        else:
            print("\n" + "=" * 70)
            print("❌ PROCESO FALLÓ")
            print("=" * 70)


def main():
    """Función principal"""
    
    print("=" * 70)
    print("🔧 HERRAMIENTA UNIFICADA DE EXCEL")
    print("   Reparar + Desproteger + Diagnosticar")
    print("=" * 70)
    
    # Parsear argumentos
    if len(sys.argv) < 2:
        archivo = input("\n📂 Ingresa el nombre del archivo Excel: ").strip('"\'')
        solo_diagnostico = False
        skip_reparacion = False
    else:
        archivo = sys.argv[1].strip('"\'')
        solo_diagnostico = '--solo-diagnostico' in sys.argv
        skip_reparacion = '--skip-reparacion' in sys.argv
    
    try:
        toolkit = ExcelToolkit(archivo)
        
        if solo_diagnostico:
            toolkit.diagnosticar()
        else:
            toolkit.proceso_completo(skip_reparacion=skip_reparacion)
        
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
    
    print("\n" + "=" * 70)
    input("\nPresiona Enter para salir...")


if __name__ == "__main__":
    main()