import base64
import logging
import socket as s
import ssl
#import sys
from time import sleep


class SMTPException(Exception):
    pass


class SMTPSessionError(SMTPException):
    pass


class SMTPServerIsNotAvailable(SMTPException):
    pass


class SMTPMailTransactionError(SMTPException):
    pass


class SMTPAuthenticationError(SMTPException):
    pass


log = logging.getLogger()
logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s'
                           u' [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


class SMTP:

    def __init__(self, is_debug=False):
        self.client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.client_socket.settimeout(2)
        self.username = ""
        self.debug = is_debug

    def open_connection(self, mailserver, disable_encrypt):
        if not disable_encrypt:
            self.client_socket = ssl.wrap_socket(
                self.client_socket, ssl_version=ssl.PROTOCOL_SSLv23)
        self.client_socket.connect(mailserver)
        self.get_recv()

    def helo(self):
        helo_command = 'EHLO Alice\r\n'
        code, recv = self.send_socket(helo_command.encode())
        if code not in [250, 235, 220, 221, 354]:
            raise SMTPSessionError(code, recv)
        return code


    def auth(self, username, password):
        if self.debug:
            log.info('try Login')

        self.username = username
        base64_str = ("\x00" + username + "\x00" + password).encode()
        base64_str = base64.b64encode(base64_str)
        auth_msg = "AUTH PLAIN ".encode() + base64_str + "\r\n".encode()
        code, recv = self.send_socket(auth_msg)

        if code != 235:
            if self.debug:
                log.error('LogError with username={0}, password={1}'.
                          format(username, password))
            raise SMTPAuthenticationError(code, 'incorrect login/password')
        if self.debug:
            log.info("Success LOGIN!")

    def send_socket(self, command):
        if not isinstance(command, bytes):
            command += '\r\n'
            command = command.encode()
        self.client_socket.sendall(command)
        code = self.get_recv()
        return code

    def get_recv(self):
        recv = self.execute_recv()

        if recv[:3] not in ['250', '235', '220', '221', '354']:
            if self.debug:
                log.warning("OK reply not recieved from server: " + recv)

        if self.debug:
            log.info(recv)

        return (int(recv[:3]), recv[3:])

    def execute_recv(self):
        count = 0
        while True:
            try:
                msg = self.client_socket.recv(1024)
            except s.timeout as e:
                err = e.args[0]
                if err == 'The read operation timed out' and count < 5:
                    sleep(1)
                    count += 1
                    #print("time out. I try to send data again")
                    continue
                else:
                    print(e)
                    #sys.exit(1)
            except s.error as e:
                print(2)
                # Something else happened, handle error, exit, etc.
                print(e)
                #sys.exit(1)
            else:
                if len(msg) == 0:
                    print('orderly shutdown on server end')
                    #sys.exit(0)
                elif len(msg) < 3:
                    print('recv incorrect format')
                    #sys.exit(0)
                else:
                    break
        recv = msg.decode()
        return recv

    def mail(self):
        code, recv = self.send_socket("MAIL FROM:<{}>".format(self.username))

    def rcptTo(self, recipient):
        code,recv = self.send_socket("RCPT TO:<{}>".format(recipient))
        return code, recv

    def data(self):
        self.send_socket("DATA")

    def sendMail(self, receivers, mail):
        reciev_error = set()
        self.mail()

        if not isinstance(receivers, list):
            receivers = list(receivers)

        for receiver in receivers:
            code, recv = self.rcptTo(receiver)
            if code not in [250, 235, 220, 221, 354]:
                if self.debug:
                    log.error("Mail not send to " + receiver)

                reciev_error.add(receiver)

        self.data()
        mail += "\r\n."
        self.send_socket(mail)
        return reciev_error

    def close(self):
        quit = "QUIT"
        self.send_socket(quit)
        self.client_socket.close()
        if self.debug:
            log.info("Connection Closed")
