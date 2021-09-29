import logging
import paramiko

class SSH:
    def __init__(self):
        pass

    def get_ssh_connection(self, ssh_machine, ssh_username):
        """Establishes a ssh connection to execute command.
        :param ssh_machine: IP of the machine to which SSH connection to be established.
        :param ssh_username: User Name of the machine to which SSH connection to be established..
        :param ssh_password: Password of the machine to which SSH connection to be established..
        returns connection Object
        """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ssh_machine, username=ssh_username, timeout=10)
        return client
      
    def run_sudo_command(self, ssh_username="andoni", ssh_password="odoo", ssh_machine="willie02.fsz", command="ls",
                         jobid="None"):
        """Executes a command over a established SSH connectio.
        :param ssh_machine: IP of the machine to which SSH connection to be established.
        :param ssh_username: User Name of the machine to which SSH connection to be established..
        :param ssh_password: Password of the machine to which SSH connection to be established..
        returns status of the command executed and Output of the command.
        """
        conn = self.get_ssh_connection(ssh_machine=ssh_machine, ssh_username=ssh_username)
        command = "sudo -S -p '%s' %s" % (ssh_password, command)
        logging.info("Job[%s]: Executing: %s" % (jobid, command))
        stdin, stdout, stderr = conn.exec_command(command=command)
        stdin.write(ssh_password + "\n")
        stdin.flush()
        stdoutput = [line for line in stdout]
        stderroutput = [line for line in stderr]
        for output in stdoutput:
            logging.info("Job[%s]: %s" % (jobid, output.strip()))
        # Check exit code.
        logging.debug("Job[%s]:stdout: %s" % (jobid, stdoutput))
        logging.debug("Job[%s]:stderror: %s" % (jobid, stderroutput))
        logging.info("Job[%s]:Command status: %s" % (jobid, stdout.channel.recv_exit_status()))
        if not stdout.channel.recv_exit_status():
            logging.info("Job[%s]: Command executed." % jobid)
            conn.close()
            if not stdoutput:
                stdoutput = True
            return True, stdoutput
        else:
            logging.error("Job[%s]: Command failed." % jobid)
            for output in stderroutput:
                logging.error("Job[%s]: %s" % (jobid, output))
            conn.close()
            return False, stderroutput