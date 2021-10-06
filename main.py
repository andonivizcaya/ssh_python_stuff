from .actualize_full import descomprimir_tar, push_github,ejecutar_n1, desconectar_usuarios, respaldar_metadata, actuatliazacion_base, enviar_archivos_war
from .actualize_full import actualizar_webapps
import datetime

def read_file(file_name):
	for row in open(file_name, 'r'):
		yield row


with open('actualizar_bases.log', 'w') as f:
    carpetas_sigad_web = []
    motor_server = ()
    motores_servers = []
    for row in read_file('./actualizar_bases.csv'):
        datos = tuple(row.replace('\n', '').split(','))

        motor, ssh_server, ruta_base, nombre_base, usuario, password, alias_base, carpeta_sigad_web = datos
        
        if carpeta_sigad_web not in carpetas_sigad_web:
            print('{} Paso 1: descomprimir .tar.bz2'.format(datetime.datetime.today()))
            f.write('{} Paso 1: descomprimir .tar.bz2'.format(datetime.datetime.today()))
            descomprimir_tar(motor, ssh_server, ruta_base, nombre_base, usuario, password, alias_base, carpeta_sigad_web)
            carpetas_sigad_web.append(carpeta_sigad_web)
            print('{} Paso 1 finalizado.\2'.format(datetime.datetime.today()))
            f.write('{} Paso 1 finalizado.\2'.format(datetime.datetime.today()))
        else:
            pass

        #push_github(motor, ssh_server, ruta_base, nombre_base, usuario, password, alias_base, carpeta_sigad_web)

        if (motor, ssh_server) not in motores_servers:
            print('{} Paso 2: ejecutar N1'.format(datetime.datetime.today()))
            f.write('{} Paso 2: ejecutar N1'.format(datetime.datetime.today()))
            ejecutar_n1(motor, ssh_server, ruta_base, nombre_base, usuario, password, alias_base, carpeta_sigad_web)
            motores_servers.append((motor, ssh_server))
            print('{} Paso 2 finalizado.\n'.format(datetime.datetime.today()))
            f.write('{} Paso 2 finalizado.\n'.format(datetime.datetime.today()))
        else:
            pass
        
        print('{} Paso 3: desconectar usuarios'.format(datetime.datetime.today()))
        f.write('{} Paso 3: desconectar usuarios'.format(datetime.datetime.today()))
        desconectar_usuarios(motor, ssh_server, ruta_base, nombre_base, usuario, password, alias_base, carpeta_sigad_web)
        print('{} Paso 3 finalizado.'.format(datetime.datetime.today()))
        f.write('{} Paso 3 finalizado.'.format(datetime.datetime.today()))

        print('{} Paso 4: respaldar metadata'.format(datetime.datetime.today()))
        f.write('{} Paso 4: respaldar metadata'.format(datetime.datetime.today()))
        respaldar_metadata(motor, ssh_server, ruta_base, nombre_base, usuario, password, alias_base, carpeta_sigad_web)
        print('{} Paso 4 finalizado.'.format(datetime.datetime.today()))
        f.write('{} Paso 4 finalizado.'.format(datetime.datetime.today()))

        print('{} Paso 5: actulizar base, actualizar version Sigad, renombrar base nuevamente'.format(datetime.datetime.today()))
        f.write('{} Paso 5: actulizar base, actualizar version Sigad, renombrar base nuevamente'.format(datetime.datetime.today()))
        actuatliazacion_base(motor, ssh_server, ruta_base, nombre_base, usuario, password, alias_base, carpeta_sigad_web)
        print('{} Paso 5 finalizado.'.format(datetime.datetime.today()))
        f.write('{} Paso 5 finalizado.'.format(datetime.datetime.today()))

    carpetas_sigad_web = []
    for row in read_file('./actualizar_bases.csv'):
        if carpeta_sigad_web not in carpetas_sigad_web:
            print('{} Paso 6: enviar archivos .war'.format(datetime.datetime.today()))
            f.write('{} Paso 6: enviar archivos .war'.format(datetime.datetime.today()))
            enviar_archivos_war(motor, ssh_server, ruta_base, nombre_base, usuario, password, alias_base, carpeta_sigad_web)
            carpetas_sigad_web.append(carpeta_sigad_web)
            print('{} Paso 6 finalizado.\2'.format(datetime.datetime.today()))
            f.write('{} Paso 6 finalizado.\2'.format(datetime.datetime.today()))
        else:
            pass
    

with open('./actualizar_webapps.log', 'w') as g:
    for row in read_file('./actualizar_webapps.csv'):
        datos = tuple(row.replace('\n', '').split(','))

        tomcat, ssh_server, archivo_war, nombre_webapp = datos
        print('{} ACTUALIZANDO WEBAPP: '.format(datetime.datetime.today()) + nombre_webapp + ' EN EL TOMCAT: ' + tomcat + ' Y SERVIDOR: ' + ssh_server)
        g.write('{} ACTUALIZANDO WEBAPP: '.format(datetime.datetime.today()) + nombre_webapp + ' EN EL TOMCAT: ' + tomcat + ' Y SERVIDOR: ' + ssh_server)
        actualizar_webapps(tomcat, ssh_server, archivo_war, nombre_webapp)
        print('{} FINALIZANDO ACTUALIZACIÓN'.format(datetime.datetime.today()))
        g.write('{} FINALIZANDO ACTUALIZACIÓN'.format(datetime.datetime.today()))