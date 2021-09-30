from utils.funcs import Funcs


#1.- Obtener lista de rutas hacia carpetas en /u/firebird25/wrk/
# Solución: usar un comando sudo_su - firebird25 que haga ls -l a /u/firebird25/wrk/ y que entregue una lista con las carpetas.
# **generar tal función en funcs

#2.- Copiar archivo .tar.bz2 (si cliente está en Edicloud) a la carpeta update_bd_AAAAMMDD
# Solución: usar la función sudo_su ya creada

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
# Solución: conectarse a firebird25.moe.etrade.cl, aplicar sudo_su con usuario firebird y pasar como argumentos cd /u/firebird25/wrk/SigadWebVersion_09082021/update_bd_20210908,
#echo $FIREBIRD, export FIREBIRD_MSG=/opt/firebird25, isql motor.dbz/3050:<ruta base>/<nombre base original> -user <usuario> -pass <password> -i <ruta a .sql>

#7.- 

Funcs.sudo_su("cd /u/firebird25/wrk/")