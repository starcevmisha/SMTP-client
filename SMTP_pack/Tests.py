import sys
import unittest
from unittest import mock

import smtp_server
from arguments1 import Arguments

import email_format

# from mock import patch

true_email = 'Content-Type: multipart/mixed; boundary="===============84847' \
             '77675788374285=="\r\nMIME-Version: 1.0\r\nFrom: smtp.task' \
             '2@gmail.com\r\nSubject: smthnew\r\nTo: starcev_misha@'\
             'mail.ru\r\n'\
             '\r\n--===============8484777675788374285==\r\nContent-Type:' \
             ' text/plain; charset="us-ascii"\r\nMIME-Version: 1.0\r\nC' \
             'ontent-Transfer-Encoding: 7bit\r\n\r\niloveyouPython\r\n--' \
             '===============8484777675788374285==--'


class TestEmailFormat(unittest.TestCase):
    test_email = email_format.Email(fromaddr="smtp.task2@gmail.com",
                                    toaddrs="starcev_misha@mail.ru",
                                    subject="smthnew",
                                    message="iloveyouPython",
                                    ).email

    def test_email_format(self):
        self.assertEqual(self.test_email, true_email)


class TestArgParse(unittest.TestCase):

    def test_arg_parse(self):
        true_dict = {
            'fromaddr': 'smtp.task2@gmail.com',
            'username': 'smtp.task2@gmail.com',
            'password': 'pythonpython',
            'toaddrs': ['starcev_misha@mail.ru'],
            'server': (
                'smtp.gmail.com',
                465),
            'data': {
                'subject': 'smthnew',
                'msg': 'iloveyouPython',
                'attach': [
                    '123.txt',
                    '12.png']},
            'mode': 'together',
            'dis_enc': False,
            'debug': False}

        sys.argv[1:] = '--server smtp.gmail.com:465 ' \
                       '--fromaddr smtp.task2@gmail.com ' \
                       '--passwd pythonpython ' \
                       '--toaddrs starcev_misha@mail.ru ' \
                       '--subj smthnew --msg iloveyouPython ' \
                       '--attach 123.txt 12.png ' \
                       '--mode together'.split(' ')
        parser = Arguments()
        args = parser.get_args()
        self.assertDictEqual(true_dict, args)


def start_smtp():
    smtp = smtp_server.SMTP()
    smtp.open_connection(('smtp.gmail.com', 465), False)
    return smtp


class TestSmtpServer(unittest.TestCase):

    def test_recv_ehlo_fail(self):
        smtp = start_smtp()
        value = (
            '501 5.5.4 Empty HELO/EHLO argument not '
            'allowed, closing connection.')
        with mock.patch.object(smtp, 'execute_recv', return_value=value):
            with self.assertRaises(smtp_server.SMTPSessionError):
                smtp.helo()
        smtp.close()

    def test_recv_ehlo_success(self):
        smtp = start_smtp()
        value = (
            '250 \n'
            '250 smtp.gmail.com at your service, [128.75.98.44]\n'
            '250-SIZE 35882577\n'
            '250-8BITMIME\n'
            '250-AUTH LOGIN PLAIN XOAUTH2 PLAIN-CLIENTTOKEN OAUTHBEARER'
            ' XOAUTH\n'
            '250-ENHANCEDSTATUSCODES\n'
            '250-PIPELINING\n'
            '250-CHUNKING\n'
            '250 SMTPUTF8\n')
        with mock.patch.object(smtp, 'execute_recv', return_value=value):
            self.assertEqual(250, smtp.helo())
        smtp.close()

    def test_recv_login_fail(self):
        smtp = start_smtp()
        smtp.helo()
        with self.assertRaises(smtp_server.SMTPAuthenticationError):
            smtp.auth("123", "123")
        smtp.close()

    def test_recv_login_succes(self):
        smtp = start_smtp()
        smtp.helo()
        value = '235 2.7.0 Accepted\r\n'
        with mock.patch.object(smtp, 'execute_recv', return_value=value):
            smtp.auth("123", "123")
        smtp.close()

    def test_send_mail(self):
        value = '250 2.1.5 OK h14sm618021lfe.30 - gsmtp\r\n'
        smtp = start_smtp()
        smtp.send_socket('.')
        self.assertEqual(1, 1)
        smtp.close()


if __name__ == '__main__':
    unittest.main()
