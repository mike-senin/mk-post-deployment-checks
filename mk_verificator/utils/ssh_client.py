import time
import select
from paramiko import SSHClient, SFTPClient, AutoAddPolicy, RSAKey

# TODO(msenin) uncomment after logging module review
# from logger import getLogger


class Node(object):

    def __init__(self, name, host, username, password=None, ssh_port=22,
                 pub_key=None):
        """
        :param name: additional field for node name, useful for nodes filter
        :param host: ip address of remote node
        :param username: username for login
        :param password: password for login
        :param ssh_port: custom ssh port
        :param pub_key: path to pub. key
        """

        self.id = name
        self.hostname = host
        self.username = username
        self.password = password
        self.ssh_port = int(ssh_port)
        self.pub_key = pub_key
        self.ssh = self.init_client()
        # TODO(msenin) uncomment after logging module review
        # self.logger = getLogger("mk_test_framework")

    def __enter__(self):
        return self

    def __exit__(self, extype, exval, trace):
        if extype:
            msg = "SSH Manager: exception"
            # TODO(msenin) uncomment after logging module review
            # self.logger.error(msg, exc_info=(extype, exval, trace))

        try:
            self.ssh.close()
        except:
            pass
            # TODO(msenin) uncomment after logging module review
            # self.logger.error(
            #     "SSH Manager: conn for %s is not closable", self.id
            # )
        finally:
            return True

    def init_client(self):
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy())

        if self.pub_key:
            pkey = RSAKey.from_private_key_file(self.pub_key)
            ssh.connect(hostname=self.hostname, username=self.username,
                        pkey=pkey, look_for_keys=True)
        elif self.password:
            ssh.connect(hostname=self.hostname, port=self.ssh_port,
                        username=self.username, password=self.password,
                        look_for_keys=True)
        else:
            raise ValueError('password or pub_key is required')

        return ssh

    def close(self):
        self.ssh.close()

    def run(self, command, sudo=False, timeout=None):
        """
        :param command: - string with bash/cli command
        :param sudo: - boolean
        :param timeout: integer value - command timeout
        :return:
        """
        if timeout:
            command = "timeout --signal=9 {0} {1}".format(timeout, command)
        if sudo:
            command = "sudo {0}".format(command)

        msg = "{0} ({1}): {2}".format(self.id, self.hostname, command)
        # TODO(msenin) uncomment after logging module review
        # self.logger.debug(msg)

        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
        except AttributeError as NoOpenSession:
            msg = "SSH Manager: no conn for {0}".format(self.id)
            # TODO(msenin) uncomment after logging module review
            # self.logger.error(msg)
            raise NoOpenSession

        out = stdout.read().strip('\n')
        err = stderr.read().strip('\n')
        result = err if err else out
        # TODO(msenin) uncomment after logging module review
        # self.logger.debug(result)

        return result

    def run_channel_command(self, command):
        client = self.ssh
        try:
            channel = client.get_transport().open_session()
            channel.exec_command(command)
            output = ''
            while True:
                if channel.exit_status_ready():
                    output = output + channel.recv(1048576)
                    break
                rl, wl, xl = select.select([channel], [], [], 0.0)
                if len(rl) > 0:
                    output = output + channel.recv(1024)
            return output
        except Exception as e:
            pass
            # TODO(msenin) uncomment after logging module review
            # self.logger.error(e)
        finally:
            client.close()

    def get(self, remotepath, localpath):
        # TODO(msenin) uncomment after logging module review
        # self.logger.debug("sftp get %s %s", remotepath, localpath)
        with SFTPClient.from_transport(self.ssh.get_transport()) as sftp:
            sftp.get(remotepath=remotepath, localpath=localpath)

    def put(self, localpath, remotepath):
        # TODO(msenin) uncomment after logging module review
        # self.logger.debug("sftp put %s %s", localpath, remotepath)
        with SFTPClient.from_transport(self.ssh.get_transport()) as sftp:
            sftp.put(localpath=localpath, remotepath=remotepath)

    def rm(self, path):
        command = "rm {0}".format(path)
        return self.run(command, sudo=True)

    def ping(self, address, interval=0.2, count=5):
        timeout = interval
        deadline = count * timeout
        start = time.time()
        ping_statistic = \
            self.run(
                "ping -w {0} -W {1} -c {2} -i {3} {4}".format(
                    deadline, timeout, count, interval, address
                )
            )
        execution_time = time.time() - start
        # TODO(msenin) uncomment after logging module review
        # self.logger.debug('Ping time: %s', execution_time)
        # self.logger.debug('Ping statistic: %s', ping_statistic)

        if '100% packet loss' in ping_statistic:
            # self.logger.error(ping_statistic)
            result = False
        else:
            result = True

        return result, ping_statistic, execution_time
