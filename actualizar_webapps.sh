#!/bin/bash
echo "Iniciando actualización SigadWeb $(date +"%d-%m-%y %T")"
echo "iniciando borrando aplicacion Valero $(date)"
cp "/home/athos/$2" "/home/$1"
chown "$1:sigadweb" "/home/$1/$2"
runuser -l $1 -c "rm -rf /home/$1/*Old"
runuser -l $1 -c "mv /home/$1/webapps/${2::-4}$3 /home/$1/${2::-4}$3Old"
echo "Iniciando copia del archivo .war a /webapps/*Cliente.war"
runuser -l $1 -c "cp /home/$1/$2 /home/$1/webapps/${2::-4}$3.war"
sleep 30
runuser -l $1 -c "cp -rf /home/$1/webapps/${2::-4}$3 /home/$1/${2::-4}$3"
runuser -l $1 -c "rm -rf /home/$1/webapps/$2"
runuser -l $1 -c "cp -rf /home/$1/${2::-4}$3Old/META-INF/context.xml /home/$1/${2::-4}$3/META-INF/context.xml"
echo "Moviendo ${2::-4}$3 a webapps/ $(date +"%d-%m-%y %T")"
runuser -l $1 -c "mv -rf /home/$1/${2::-4}$3 /home/$1/webapps/"
sleep 30
echo "Proceso finalizado para el cliente $3"