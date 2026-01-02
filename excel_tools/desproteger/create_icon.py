"""
Generador de ícono para la aplicación Excel Tool
Requiere: pip install pillow
"""

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("❌ Error: Pillow no está instalado")
    print("Instálalo con: pip install pillow")
    input("\nPresiona Enter para salir...")
    exit(1)

def crear_icono():
    """Crea un ícono simple para la aplicación"""
    
    print("🎨 Creando ícono de la aplicación...")
    
    # Crear imagen de 256x256 (tamaño recomendado para íconos)
    size = 256
    img = Image.new('RGBA', (size, size), color=(37, 99, 235, 0))  # Fondo transparente
    draw = ImageDraw.Draw(img)
    
    # Fondo circular azul
    margin = 20
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill=(37, 99, 235, 255),  # Azul
        outline=(29, 78, 216, 255),
        width=8
    )
    
    # Dibujar símbolo de Excel (E estilizada)
    try:
        # Intentar usar una fuente del sistema
        font_size = 140
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("segoeui.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        # Texto "E" (de Excel)
        text = "E"
        
        # Calcular posición centrada
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size - text_width) // 2 - 5
        y = (size - text_height) // 2 - 15
        
        # Dibujar texto con sombra
        shadow_offset = 4
        draw.text((x + shadow_offset, y + shadow_offset), text, fill=(0, 0, 0, 128), font=font)
        draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
        
    except Exception as e:
        print(f"⚠️  No se pudo agregar texto: {e}")
    
    # Agregar "herramienta" visual (llave inglesa pequeña)
    wrench_color = (255, 255, 255, 255)
    
    # Mango de la llave
    draw.rectangle([180, 160, 190, 220], fill=wrench_color)
    
    # Cabeza de la llave
    draw.ellipse([175, 145, 195, 165], fill=wrench_color)
    draw.ellipse([180, 150, 190, 160], fill=(37, 99, 235, 255))  # Agujero
    
    # Guardar como ICO (formato de ícono de Windows)
    ico_path = "excel_tool.ico"
    
    # Crear versiones en múltiples tamaños para el ICO
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    images = []
    
    for size_tuple in sizes:
        resized = img.resize(size_tuple, Image.Resampling.LANCZOS)
        images.append(resized)
    
    # Guardar como ICO multi-resolución
    images[0].save(
        ico_path,
        format='ICO',
        sizes=[(img.width, img.height) for img in images],
        append_images=images[1:]
    )
    
    print(f"✅ Ícono creado exitosamente: {ico_path}")
    print(f"📁 Resoluciones incluidas: {', '.join([f'{s[0]}x{s[1]}' for s in sizes])}")
    
    # También guardar como PNG para preview
    img.save("excel_tool_preview.png", format='PNG')
    print(f"✅ Preview guardado como: excel_tool_preview.png")
    
    return ico_path


if __name__ == "__main__":
    print("=" * 60)
    print("🎨 GENERADOR DE ÍCONO - EXCEL TOOL")
    print("=" * 60)
    print()
    
    try:
        ico_file = crear_icono()
        print()
        print("=" * 60)
        print("✅ ¡Ícono creado con éxito!")
        print("=" * 60)
        print()
        print("💡 Ahora puedes usar este ícono al crear el ejecutable")
        print(f"   con PyInstaller usando: --icon={ico_file}")
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ Error al crear ícono: {e}")
        print("=" * 60)
    
    print()
    input("Presiona Enter para salir...")