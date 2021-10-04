from utils.funcs import Funcs
from datetime import date
import pexpect
import subprocess
import os
import sys
import csv


## Parte 1
# Actualizar esquema de base de datos
def actualizar_bases(motor, ssh_server, ruta_base, nombre_base, usuario, password, alias_base, carpeta_sigad_web):

    #1.- Copiar archivo .tar.bz2 (si cliente está en Edicloud) a la carpeta update_bd_AAAAMMDD
    # Solución: usar la función sudo_su ya creada
    
    ddmmaaaa = carpeta_sigad_web.split('SigadWebVersion_')[1]
    aaaammdd = ddmmaaaa[4:] + ddmmaaaa[2:4] + ddmmaaaa[:2]

    ruta_sigad_web = "/u/firebird25/wrk/" + carpeta_sigad_web
    update_bd = "update_bd_" + aaaammdd
    ruta_update_bd = ruta_sigad_web + "/" + update_bd

    upd_database = []
    webapps = []
    wrk_list = os.listdir(ruta_sigad_web)

    for file in wrk_list:
        if file.__contains__('.war'):
            webapps.append(file)
        elif file.__contains__('tar.bz2'):
            upd_database.append(file)

    if len(upd_database) == 1:
        subprocess.Popen(["mkdir", update_bd], cwd=ruta_sigad_web)
        subprocess.Popen(["cp", upd_database[0], update_bd], cwd=ruta_sigad_web)
        subprocess.Popen(["bzip2", "-b", upd_database[0]], cwd=ruta_update_bd)
        subprocess.Popen(["tar", "-xvf", upd_database[0].replace(".bz2", "")], cwd=ruta_update_bd)
    else:
        print('Más de un archivo .tar.bz2')

    #Funcs.sudo_su("git add /u/firebird25/wrk/*", commit, "git push origin main")
def push_github(motor, ssh_server, ruta_base, nombre_base, usuario, password, alias_base, carpeta_sigad_web):

    ddmmaaaa = carpeta_sigad_web.split('SigadWebVersion_')[1]
    aaaammdd = ddmmaaaa[4:] + ddmmaaaa[2:4] + ddmmaaaa[:2]

    ruta_sigad_web = "/u/firebird25/wrk/" + carpeta_sigad_web
    update_bd = "update_bd_" + aaaammdd
    ruta_update_bd = ruta_sigad_web + "/" + update_bd
    #2.- Obtener lista de rutas hacia carpetas en /u/firebird25/wrk/
    # Solución: usar un comando sudo_su - firebird25 que haga ls -l a /u/firebird25/wrk/ y que entregue una lista con las carpetas.
    # **generar tal función en funcs

    commit = "\"update-{}\"".format(date.today().strftime("%Y%m%d"))

    Funcs.git_push("/u/firebird25/wrk/", commit)
    #Funcs.git_push('/u/firebird25/wrk/', commit)

    #Funcs.sudo_su()

def ejecutar_n1(motor, ssh_server, ruta_base, nombre_base, usuario, password, alias_base, carpeta_sigad_web):

    #ddmmaaaa = carpeta_sigad_web.split('SigadWebVersion_')[1]
    #aaaammdd = ddmmaaaa[4:] + ddmmaaaa[2:4] + ddmmaaaa[:2]

    #ruta_sigad_web = "/u/firebird25/wrk/" + carpeta_sigad_web
    #update_bd = "update_bd_" + aaaammdd
    #ruta_update_bd = ruta_sigad_web + "/" + update_bd
    #3.- Ejecutar respaldo N1 modificando el cron
    # Solución: usar sudo_su y pasar como parámetro comando para modificar cron (ver func -> modify_cron)

    client = Funcs.connect_ssh(ssh_server, 'bkp-firebird')
    Funcs.modify_cron(client, motor)

    client.close()

def desconectar_usuarios(motor, ssh_server, ruta_base, nombre_base, usuario, password, alias_base, carpeta_sigad_web):

    ddmmaaaa = carpeta_sigad_web.split('SigadWebVersion_')[1]
    aaaammdd = ddmmaaaa[4:] + ddmmaaaa[2:4] + ddmmaaaa[:2]

    ruta_sigad_web = "/u/firebird25/wrk/" + carpeta_sigad_web
    update_bd = "update_bd_" + aaaammdd
    ruta_update_bd = ruta_sigad_web + "/" + update_bd
    #4.- Desconectar usuarios
    # Solución: conectarse al servidor rod.fsz, todd.fsz o ned.fsz, usar sudo_su al usuario bkp-frebird, mover la base.
    # Luego desconectarse y hacer sudo_su a root pasando como argumento el comandoo fuserk <ruta base>/<nombre base original>.
    # Desconectarse de root y usar sudo_su a bkp-firebird con argumentos cd ~/bkp_bases, mkdir AAAMMDD, cp <ruta base>/<nombre base original> /home/bkp-firebird/bkp_bases /AAAAMMDD/

    mv_desde = ruta_base + "/" + nombre_base
    nombre_base_original = nombre_base.replace('.fdb', '_offline.fdb')
    mv_hacia = ruta_base + "/" + nombre_base_original

    client = Funcs.connect_ssh(ssh_server, 'bkp-firebird')
    stdin, stdout,stderr = client.exec_command("mv " + mv_desde + " " + mv_hacia)
    stdin.close()
    stdout.close()
    stderr.close()

    client.close()

    ssh_pass = 'Sprt.1215'

    client = Funcs.connect_ssh('localhost', 'athos', ssh_pass)
    command = "fuser -k " + ruta_base + "/" + nombre_base + " " + ruta_base + "/" + nombre_base_original
    bkp_base = "/home/bkp-firebird/bkp_bases/" + aaaammdd
    Funcs.sudo_su(client, command)

    client.close()

    client = Funcs.connect_ssh(ssh_server, 'bkp-firebird')
    stdin, stdout,stderr = client.exec_command("mkdir " +  bkp_base)
    stdin.close()
    stdout.close()
    stderr.close()
    stdin, stdout,stderr = client.exec_command("cp " + mv_hacia + " " + bkp_base + "/")
    stdin.close()
    stdout.close()
    stderr.close()

    client.close()


def respaldar_metadata(motor, ssh_server, ruta_base, nombre_base, usuario, password, alias_base, carpeta_sigad_web):

    ddmmaaaa = carpeta_sigad_web.split('SigadWebVersion_')[1]
    aaaammdd = ddmmaaaa[4:] + ddmmaaaa[2:4] + ddmmaaaa[:2]

    ruta_sigad_web = "/u/firebird25/wrk/" + carpeta_sigad_web
    update_bd = "update_bd_" + aaaammdd
    ruta_update_bd = ruta_sigad_web + "/" + update_bd

    bkp_base = "/home/bkp-firebird/bkp_bases/" + aaaammdd

    nombre_base_original = nombre_base.replace('.fdb', '_offline.fdb')
    letra = motor[-1]
    #5.- Respaldar metadata base
    # Solución: conectarse al servidor rod.fsz, todd.fsz o ned.fsz, usar sudo_su al usuario bkp_frebird.
    # Pasar como argumentos cd ~, ls setEnvFB25*.env y listar las variables de ambiente.
    # Conectarse nuevamente pero esta vez con la función sud_su normal y pasar como argumento source setEnvFB25<letra>.env y el comando isql -x.

    client = Funcs.connect_ssh(ssh_server, 'bkp-firebird')
    stdin, stdout,stderr = client.exec_command("source setEnvFB25" + letra + ".env")
    stdin.close()
    stdout.close()
    stderr.close()
    stdin, stdout,stderr = client.exec_command("isql -x " + ruta_base + " -user " + usuario + " -password " + password + " -o " + bkp_base + "/respaldo_metadata_" + alias_base + "_" + ddmmaaaa + ".sql")
    stdin.close()
    stdout.close()
    stderr.close()

    client.close()

def actuatliazacion_base(motor, ssh_server, ruta_base, nombre_base, usuario, password, alias_base, carpeta_sigad_web):

    ddmmaaaa = carpeta_sigad_web.split('SigadWebVersion_')[1]
    aaaammdd = ddmmaaaa[4:] + ddmmaaaa[2:4] + ddmmaaaa[:2]

    ruta_sigad_web = "/u/firebird25/wrk/" + carpeta_sigad_web
    update_bd = "update_bd_" + aaaammdd
    ruta_update_bd = ruta_sigad_web + "/" + update_bd

    upd_database = []
    webapps = []
    wrk_list = os.listdir(ruta_sigad_web)

    for file in wrk_list:
        if file.__contains__('.war'):
            webapps.append(file)
        elif file.__contains__('tar.bz2'):
            upd_database.append(file)

    nombre_base_original = nombre_base.replace('.fdb', '_offline.fdb')
    #6.- Ejecutar actualización base
    # Solución: conectarse a firebird25.moe.etrade.cl, aplicar sudo_su con usuario firebird25 y pasar como argumentos cd /u/firebird25/wrk/SigadWebVersion_09082021/update_bd_20210908,
    #echo $FIREBIRD, export FIREBIRD_MSG=/opt/firebird25, isql motor.dbz/3050:<ruta base>/<nombre base original> -user <usuario> -pass <password> -i <ruta a .sql>
    subprocess.Popen(["export", "FIREBIRD_MSG=/opt/firebird25"])
    process = subprocess.Popen(["isql", motor + ".dbz/3050:" + ruta_base + "/" + nombre_base_original, "-user", usuario, "-password", password, "-i", upd_database[0].replace("tar.bz2", "sql")], stdout=subprocess.PIPE, stderr=subprocess.STDOUT , cwd=ruta_update_bd)
    with open(ruta_update_bd + '/log_isql.log', 'w') as f:
        for line in process.stdout:
            f.write(line.decode('utf-8'))
        process.wait()

    with open(ruta_update_bd + '/log_isql.log', 'r') as f:
        lines = f.readlines()
        for line in lines[-5:]:
            if line.__contains__('deadlock'):
                subprocess.Popen(["isql", motor + ".dbz/3050:" + ruta_base + "/" + nombre_base_original, "-user", usuario, "-password", password, "-i", upd_database[0].replace("tar.bz2", "sql")])

    #7.- Actualizar versión Sigad
    # Solución: conectarse a firebird25.moe.etrade.cl, aplicar sudo_su con usuario firebird25 y pasar como argumentos
    # isql motor.dbz/3050:<ruta base>/<nombre base original> -user <usuario> -pass <password> -i /u/firebird25/wrk/SigadWebVersion_20092021/upd_version.sql
    # upd_version.sql se encuentra en la ruta original del update

    subprocess.Popen(["isql", motor, ".dbz/3050:" + ruta_base + "/" + nombre_base_original, "-user", usuario, "-password", password, "-i", "upd_version.sql"], cwd=ruta_sigad_web)

    #8.- Renombrar base nuevamente
    # Solución: conectarse a rod.fsz, todd.fsz o ned.fsz con el usuario athos, hacer sudo_su al uduario bkp-firebird con los argumentos cd <ruta_base> mv <nombre base original> <nombre base>

    subprocess.Popen(["mv", nombre_base_original, nombre_base], cwd=ruta_base)


## Parte 2
# Actualizar WebApps
def actualize_webapps(motor, ssh_server, ruta_base, nombre_base, usuario, password, alias_base, carpeta_sigad_web):
    ruta_sigad_web = "/u/firebird25/wrk/" + carpeta_sigad_web

    files = os.listdir(ruta_sigad_web)
    client = Funcs.connect_ssh('johnny.fsz', 'athos')
    for file in files:
        if file.__contains__('.war'):

            sftp = client.open_sftp()
            sftp.put(ruta_sigad_web + '/' + file, '/home/athos/'+ file)
            sftp.close()

            #client.exec_command()


    #enviar al jimmy la aplicación comprimida




def read_file(file_name):
	for row in open(file_name, 'r'):
		yield row


for row in read_file('./actualizar1.csv'):
    print(row.replace('\n', ''))




#ejecutar_n1(motor='echocito.sh', ssh_server='willie02.fsz', ruta_base=None, nombre_base=None, usuario=None, password=None, alias_base=None, carpeta_sigad_web=None)
