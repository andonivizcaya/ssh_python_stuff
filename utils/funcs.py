from typing import Coroutine
from paramiko import SSHClient
from paramiko.client import AutoAddPolicy
from rich import pretty, inspect
import subprocess
from subprocess import Popen
import pexpect
from git import Repo
pretty.install()


class Funcs:


    def connect_ssh(ssh_server, ssh_user):
        client = SSHClient()

        # Load Host Keys
        client.load_host_keys('/home/avizcaya/.ssh/known_hosts')
        client.load_system_host_keys()

        # known_hosts policy
        client.set_missing_host_key_policy(AutoAddPolicy())

        client.connect(ssh_server, username='ssh_user')

        return client

    # funtion that a modifies existing cronjob
    def modify_cron(client):

        # get all cron
        stdin, stdout, stderr = client.exec_command('crontab -l')
        cron_list = stdout.read().decode('utf-8').split('\n')

        for line in cron_list:
            if line.__contains__('magico1'):
                i = cron_list.index(line)
                cron_list[i + 1] = '#' + cron_list[i + 1]
            if line.__contains__('magico2'):
                i = cron_list.index(line)
                cron_list[i + 1] = '5' + cron_list[i + 1][1:]

        # Remove all cron
        stdin, stdout, stderr = client.exec_command('echo " " | crontab -')

        # add moddified cron
        for new_line in cron_list:
            stdin, stdout, stderr = client.exec_command(f'crontab -l 2>/dev/null| cat - <(echo "{new_line}") | crontab -')

        stdin.close()
        stdout.close()
        stderr.close()

        client.close()


    # funtion that creates new cronjob
    def write_cron(client):
        #create new cron
        new_cron = '* * * * * somethin.something >> something.log 2>&1'
        stdin, stdout, stderr = client.exec_command(f'crontab -l 2>/dev/null| cat - <(echo "{new_cron}") | crontab -')

        stdin.close()
        stdout.close()
        stderr.close()

        client.close()


    def sudo_su_list(client, *args, **kwargs):

        command = ""
        for arg in args:
            command = command + arg + ";"

        full_command = "expect -c 'spawn sudo su - -c " + "\"" + command + "\" " + remote_server_2_username + ";expect password;send \"" + remote_server_2_password + "\r\""

        # make sudo su - user commands
        stdin_, stdout_, stderr_ = client.exec_command(full_command, get_pty=True)
        status_ = stdout_.channel.recv_exit_status()

        lista_de_weas = stdout_.read().decode("utf-8").split('\n')[3:]
        lista_de_otras_weas = []
        for wea in lista_de_weas:
            print(wea)
            lista_de_otras_weas.append(wea.split(' ')[-1].replace('\r', ''))

        print(f'STDOUT: {stdout_.read().decode("utf-8")}')
        print(f'STDERR: {stderr_.read().decode("utf-8")}')

        (lista_de_otras_weas)

        stdin_.close()
        stdout_.close()
        stderr_.close()

        client.close()


    # function to make scp between remote servers
    def scp(client, *args,**kwargs):

        command = ""
        for arg in args:
            command = command + arg + ";"
        # Initialize constructor
        
        # data (As parameters. Eg: def scp_function(filename, remote_server_2_username, remote_server_2, remote_server_2_password):)
        # exec_command("cd /u/firebird25/wrk/SigadWebVersion_09082021/;expect -c 'spawn scp ./" + "...")
        filename = "echocito"
        remote_server_2_username = "my_username"
        remote_server_2 = "my_local_host"
        remote_server_2_password = "my_pass"

        full_command = "expect -c 'spawn sudo su - -c " + "\"" + command + "\" " + remote_server_2_username + ";expect password;send \"" + remote_server_2_password + "\r\";interact';"
        full_command_scp = "expect -c 'spawn scp ./" + filename + ".log " + remote_server_2_username + "@" + remote_server_2 + ":/home/"+ remote_server_2_username +";expect password;send \"" + remote_server_2_password + "\r\";interact'"

        # scp to local machine. Use f"{command}" to execute a series of commands
        stdin_, stdout_, stderr_ = client.exec_command("expect -c 'spawn scp ./" + filename + ".log " + remote_server_2_username + "@" + remote_server_2 + ":/home/"+ remote_server_2_username +";expect password;send \"" + remote_server_2_password + "\r\";interact'", get_pty=True)
        status_ = stdout_.channel.recv_exit_status()

        print(f'STDOUT: {stdout_.read().decode("utf-8")}')
        print(f'STDERR: {stderr_.read().decode("utf-8")}')

        stdin_.close()
        stdout_.close()
        stderr_.close()

        client.close()


    # function to execute commands as another user using sudo su
    def sudo_su(*args, **kwargs):

        command = ""
        for arg in args:
            command = command + arg + ";"

        # Initialize constructor
        client = SSHClient()

        # data (As parameters. Eg: def sudo_su(filename, remote_server_2_username, remote_server_2, remote_server_2_password):)
        # exec_command("cd /u/firebird25/wrk/SigadWebVersion_09082021/;expect -c 'spawn scp ./" + "...")
        filename = "echocito"
        remote_server_2_username = "odoo"
        remote_server_2 = "192.168.7.46"
        remote_server_2_password = "odoo"

        # Load Host Keys
        client.load_host_keys('/home/avizcaya/.ssh/known_hosts')
        client.load_system_host_keys()

        # known_hosts policy
        client.set_missing_host_key_policy(AutoAddPolicy())

        client.connect(remote_server_2, username='andoni')

        full_command = "expect -c 'spawn sudo su - -c " + "\"" + command + "\" " + remote_server_2_username + ";expect password;send \"" + remote_server_2_password + "\r\""

        # make sudo su - user commands
        stdin_, stdout_, stderr_ = client.exec_command(full_command, get_pty=True)
        status_ = stdout_.channel.recv_exit_status()

        # lista_de_weas = stdout_.read().decode("utf-8").split('\n')[3:]
        # lista_de_otras_weas = []
        # for wea in lista_de_weas:
        #     print(wea)
        #     lista_de_otras_weas.append(wea.split(' ')[-1].replace('\r', ''))

        print(f'STDOUT: {stdout_.read().decode("utf-8")}')
        print(f'STDERR: {stderr_.read().decode("utf-8")}')

        #(lista_de_otras_weas)

        stdin_.close()
        stdout_.close()
        stderr_.close()

        client.close()


    def git_push(path_to_repo, commit):
        try:
            repo = Repo(path_to_repo)
            repo.git.add(update=True)
            repo.index.commit(commit)
            origin = repo.remote(name='origin')
            origin.push('main')
        except:
            print('Problemas al hacer push.')

