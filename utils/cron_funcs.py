from paramiko import SSHClient
from paramiko.client import AutoAddPolicy
from rich import pretty, inspect
pretty.install()

# Initialize constructor
client = SSHClient()

# Load Host Keys
client.load_host_keys('/home/avizcaya/.ssh/known_hosts')
client.load_system_host_keys()

# known_hosts policy
client.set_missing_host_key_policy(AutoAddPolicy())

client.connect('willie02.fsz', username='andoni')

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

# add new cron
for new_line in cron_list:
    stdin, stdout, stderr = client.exec_command(f'crontab -l 2>/dev/null| cat - <(echo "{new_line}") | crontab -')

stdin.close()
stdout.close()
stderr.close()

client.close()