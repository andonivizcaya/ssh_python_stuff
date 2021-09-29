from paramiko import SSHClient
from paramiko.client import AutoAddPolicy
from rich import pretty, inspect
pretty.install()

# Initialize constructor
client = SSHClient()

# data (As parameters. Eg: def scp_function(filename, remote_server_2_username, remote_server_2, remote_server_2_password):)
# exec_command("cd /u/firebird25/wrk/SigadWebVersion_09082021/;expect -c 'spawn scp ./" + "...")
filename = "echocito"
remote_server_2_username = "my_username"
remote_server_2 = "my_local_host"
remote_server_2_password = "my_pass"

# Load Host Keys
client.load_host_keys('/home/avizcaya/.ssh/known_hosts')
client.load_system_host_keys()

# known_hosts policy
client.set_missing_host_key_policy(AutoAddPolicy())

client.connect('willie02.fsz', username='andoni')

# scp to local machine
stdin_, stdout_, stderr_ = client.exec_command("expect -c 'spawn scp ./" + filename + ".log " + remote_server_2_username + "@" + remote_server_2 + ":/home/"+ remote_server_2_username +";expect password;send \"" + remote_server_2_password + "\r\";interact'", get_pty=True)
status_ = stdout_.channel.recv_exit_status()

print(f'STDOUT: {stdout_.read().decode("utf-8")}')
print(f'STDERR: {stderr_.read().decode("utf-8")}')

stdin_.close()
stdout_.close()
stderr_.close()

client.close()