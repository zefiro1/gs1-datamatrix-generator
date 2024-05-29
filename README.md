GS1 Data Matrix Generator
Este proyecto es una aplicación de escritorio en Python que permite generar códigos GS1 Data Matrix a partir 
de información proporcionada por el usuario. La aplicación también permite visualizar el código 
generado y guardarlo en una ubicación especificada por el usuario.

Requisitos
Para ejecutar este proyecto, necesitas tener instalados los siguientes paquetes:

Python 3.7 o superior
Tkinter (incluido con la mayoría de las distribuciones de Python)
Segno
Pillow
Puedes instalar los paquetes necesarios usando pip:

```sh
pip install segno pillow
```
Uso
Sigue estos pasos para ejecutar la aplicación:

Clona este repositorio o descarga los archivos necesarios.

```sh
git clone https://github.com/tu-usuario/gs1-datamatrix-generator.git
cd gs1-datamatrix-generator
```
Ejecuta el script main.py.

```sh
python main.py
```
Introduce los datos necesarios en la interfaz de usuario:

Product Code (PC)
Serial Number (SN)
Lote (Batch)
Exp Date (CAD)
National Code (NHRN)
Haz clic en el botón "Generate" para generar y visualizar el código Data Matrix.

Haz clic en el botón "Download" para guardar el código Data Matrix en tu equipo.
