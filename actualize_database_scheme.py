from utils.funcs import Funcs
from datetime import date
import pexpect


#1.- Obtener lista de rutas hacia carpetas en /u/firebird25/wrk/
# Solución: usar un comando sudo_su - firebird25 que haga ls -l a /u/firebird25/wrk/ y que entregue una lista con las carpetas.
# **generar tal función en funcs

commit = "\"update-{}\"".format(date.today().strftime("%Y%m%d"))

Funcs.git_push('./', commit)

#Funcs.sudo_su("git add /u/firebird25/wrk/*", commit, "git push origin main")

#2.- Copiar archivo .tar.bz2 (si cliente está en Edicloud) a la carpeta update_bd_AAAAMMDD
# Solución: usar la función sudo_su ya creada

#Funcs.sudo_su()

#3.- Ejecutar respaldo N1 modificando el cron
# Solución: usar sudo_su y pasar como parámetro comando para modificar cron (ver func -> modify_cron)

#4.- Desconectar usuarios
# Solución: conectarse al servidor rod.fsz, todd.fsz o ned.fsz, usar sudo_su al usuario bkp_frebird, mover la base.
# Luego desconectarse y hacer sudo_su a root pasando como argumento el comandoo fuserk <ruta base>/<nombre base original>.
# Desconectarse de root y usar sudo_su a bkp-firebird con argumentos cd ~/bkp_bases, mkdir AAAMMDD, cp <ruta base>/<nombre base original> /home/bkp-firebird/bkp_bases /AAAAMMDD/

#5.- Respaldar metadata base
# Solución: conectarse al servidor rod.fsz, todd.fsz o ned.fsz, usar sudo_su al usuario bkp_frebird.
# Pasar como argumentos cd ~, ls setEnvFB25*.env y listar las variables de ambiente.
# Conectarse nuevamente pero esta vez con la función sud_su normal y pasar como argumento source setEnvFB25<letra>.env y el comando isql -x.

#6.- Ejecutar actualización base
# Solución: conectarse a firebird25.moe.etrade.cl, aplicar sudo_su con usuario firebird25 y pasar como argumentos cd /u/firebird25/wrk/SigadWebVersion_09082021/update_bd_20210908,
#echo $FIREBIRD, export FIREBIRD_MSG=/opt/firebird25, isql motor.dbz/3050:<ruta base>/<nombre base original> -user <usuario> -pass <password> -i <ruta a .sql>

#7.- Actualizar versión Sigad
# Solución: conectarse a firebird25.moe.etrade.cl, aplicar sudo_su con usuario firebird25 y pasar como argumentos
# isql motor.dbz/3050:<ruta base>/<nombre base original> -user <usuario> -pass <password> -i /u/firebird25/wrk/SigadWebVersion_20092021/upd_version.sql
# upd_version.sql se encuentra en la ruta original del update

#8.- Renombrar base nuevamente
# Solución: conectarse a rod.fsz, todd.fsz o ned.fsz con el usuario athos, hacer sudo_su al uduario bkp-firebird con los argumentos cd <ruta_base> mv <nombre base original> <nombre base>
