from utils.funcs import Funcs
from utils import *


#1.- Actualización de aplicaciones (cada archivo .war corresponde a una aplicación)
# Problema: no se puede aplicar sudo_su con scp, ya que ambos esperan una contraseña.
# Solución: copiar las carpetas en /u/firebird25/wrk/ a un repositorio en github. Luego hacer un pull y un push según corresponda
# En este caso se debe hacer un pull desde jonny.fsz (mediante sudo_su) con el usuario athos apuntando a /home/athos a todos los archivos .war.
# Usar una serie de comandos como argumentos de sudo_su para cada archivo .war.

Funcs.sudo_su("pwd", "ls -lh")