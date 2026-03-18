import os
import sys
import subprocess
import platform

# --- COLORES PARA LA TERMINAL ---
class Style:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def setup_venv():
    """Crea y reinicia en entorno virtual aislado."""
    venv_dir = os.path.join(os.path.dirname(__file__), "venv_v2")
    if not hasattr(sys, 'real_prefix') and not (sys.base_prefix != sys.prefix):
        if not os.path.exists(venv_dir):
            print(f"{Style.CYAN}📦 Primera ejecución: Creando entorno aislado (venv)...{Style.RESET}")
            subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
        
        python_venv = os.path.join(venv_dir, "Scripts", "python.exe")
        os.execl(python_venv, python_venv, os.path.abspath(__file__))

def setup_windows_auto():
    """Verifica e instala Tesseract en Windows automáticamente con Winget."""
    if platform.system() != "Windows": return
    
    print(f"{Style.CYAN}🔍 Verificando motor OCR (Tesseract)...{Style.RESET}")
    tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    if not os.path.exists(tesseract_path):
        print(f"{Style.YELLOW}📦 Instalando Tesseract vía Winget...{Style.RESET}")
        print(f"{Style.CYAN}⚠️ Por favor, si aparece una ventana de confirmación, acepta los permisos.{Style.RESET}")
        try:
            subprocess.run(["winget", "install", "-e", "--id", "UB-Mannheim.TesseractOCR"], check=True)
            os.environ["PATH"] += os.pathsep + r'C:\Program Files\Tesseract-OCR'
        except Exception as e:
            print(f"{Style.RED}❌ Error con Winget. Descárgalo desde: https://github.com/UB-Mannheim/tesseract/wiki{Style.RESET}")
            sys.exit(1)
    else:
        os.environ["PATH"] += os.pathsep + os.path.dirname(tesseract_path)

def install_python_libs():
    """Instala las librerías de OCR y Fotografía."""
    libs = ['ocrmypdf', 'pymupdf', 'Pillow']
    for lib in libs:
        try:
            __import__(lib if lib != 'pymupdf' else 'fitz')
        except ImportError:
            print(f"{Style.YELLOW}📥 Instalando {lib}...{Style.RESET}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib, "--quiet"])

def aplicar_filtros_vision(archivo_entrada, archivo_temporal):
    """Extrae páginas, aplica filtros fotográficos de alto contraste y crea un PDF temporal."""
    import fitz
    from PIL import Image, ImageEnhance
    
    print(f"{Style.CYAN}📸 Fase 1: Aplicando filtros de visión artificial para resaltar letras...{Style.RESET}")
    doc = fitz.open(archivo_entrada)
    imagenes = []
    
    for num_pagina in range(len(doc)):
        pagina = doc.load_page(num_pagina)
        pix = pagina.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Filtros de imagen: Oscurecer fondo, reventar contraste y afilar bordes
        img = ImageEnhance.Brightness(img).enhance(0.7)
        img = ImageEnhance.Contrast(img).enhance(2.5)
        img = ImageEnhance.Sharpness(img).enhance(2.0)
        
        imagenes.append(img)
    
    # Guardar en PDF temporal
    imagenes[0].save(archivo_temporal, save_all=True, append_images=imagenes[1:])
    doc.close()

def main():
    import ocrmypdf
    print(f"\n{Style.BOLD}{Style.GREEN}🧠 PDF OCR VISION V2 (Alto Contraste) 🧠{Style.RESET}")
    
    pdfs = [f for f in os.listdir('.') if f.lower().endswith('.pdf') and not f.startswith('BUSCABLE_')]
    
    if not pdfs:
        print(f"{Style.RED}❌ No hay archivos .pdf en esta carpeta.{Style.RESET}")
        input("Presiona Enter para salir...")
        return

    for i, f in enumerate(pdfs, 1): print(f"  [{i}] {f}")
    choice = input(f"\n{Style.BOLD}👉 Elige el número del archivo: {Style.RESET}")
    
    try:
        file_in = pdfs[int(choice) - 1]
        file_temp = "temp_vision.pdf"
        file_out = f"BUSCABLE_V2_{file_in}"
        
        # 1. Aplicar filtros a las imágenes
        aplicar_filtros_vision(file_in, file_temp)
        
        # 2. Leer con OCR el archivo modificado
        print(f"{Style.CYAN}🔍 Fase 2: Escaneando textos con IA...{Style.RESET}")
        try:
            ocrmypdf.ocr(file_temp, file_out, language="spa+eng", deskew=True, force_ocr=True, tesseract_pagesegmode=11, progress_bar=True)
        except Exception as e:
            if "spa" in str(e):
                print(f"{Style.YELLOW}⚠️ Reintentando solo con inglés...{Style.RESET}")
                ocrmypdf.ocr(file_temp, file_out, language="eng", deskew=True, force_ocr=True, tesseract_pagesegmode=11, progress_bar=True)
            else: raise e

        # 3. Borrar el archivo feo temporal
        if os.path.exists(file_temp): os.remove(file_temp)
        
        print(f"\n{Style.GREEN}✅ ¡LISTO! Creado: {file_out}{Style.RESET}")
    
    except Exception as e:
        print(f"\n{Style.RED}⚠ Error: {e}{Style.RESET}")
        if os.path.exists("temp_vision.pdf"): os.remove("temp_vision.pdf")
        
    input(f"\n{Style.YELLOW}Presiona Enter para cerrar...{Style.RESET}")

if __name__ == "__main__":
    setup_venv()
    setup_windows_auto()
    install_python_libs()
    main()
