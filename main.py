import csv


def read_file(file_name):
	for row in open(file_name, 'r'):
		yield row

for row in read_file('./actualizar1.csv'):
    datos = tuple(row.replace('\n', '').split(','))

    motor, ssh_server, ruta_base, nombre_base, usuario, password, alias_base, carpeta_sigad_web = datos
    
    print(ruta_base)