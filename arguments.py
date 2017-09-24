import argparse
import sys
from getpass import getpass


class Arguments:

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-s', '--server', action='store', type=str,
                                 help='SMTP server', required=True)
        self.parser.add_argument('-f', '--fromaddr', action='store', type=str,
                                 help='From address', required=True)
        self.parser.add_argument('-p', '--passwd', action='store', type=str,
                                 help='Password for login')
        self.parser.add_argument('-t,', '--toaddrs', nargs='*',
                                 help='To addresses')
        self.parser.add_argument('--subj', action='store', type=str,
                                 help='Subject of the message')
        self.parser.add_argument('-m', '--msg', action='store', type=str,
                                 help='Message for recipients')
        self.parser.add_argument('-a', '--attach', nargs='*',
                                 help='Attachments for email')
        self.parser.add_argument('--mode', action='store', type=str,
                                 choices=['separate', 'together', 'group'],
                                 help='Distribution mode')
        self.parser.add_argument('--dis-enc', action='store_true',
                                 help='disable encryption')
        self.parser.add_argument('--debug', action='store_true',
                                 help='Debug Mode')

    def get_args(self):
        args = self.parser.parse_args()
        server = input('Write your smtp serve rand port '
                       'like "smtp.gmail.com:465"') \
            if not args.server else args.server

        server, port = server.rsplit(':')
        port = int(port)

        fromaddr = input('From: ') if not args.fromaddr else args.fromaddr
        username = fromaddr
        passwd = getpass('Password: ') if not args.passwd else args.passwd

        if not args.mode:
            # print("""enter mode
            # [separate] - Distribute to everyone together
            # [together] - Distribute by group, Write each group in brackets
            # [group] - Distribute to everyone separately\n""")
            # mode = input("Mode: ")
            mode = 'together'
        else:
            mode = args.mode

        if mode not in ['separate', 'together', 'group']:
            print('mode not in [separate, together, group]')
            sys.exit()

        toaddrs = input('To: ').split(' ') \
            if not args.toaddrs else args.toaddrs
        subject = input('Subject: ') if not args.subj else args.subj

        # TODO убрать коменатарий!! разкоменть
        if not args.msg:
            msg = ''
            print('Enter message: (end with ^Z or ^D)')
            for line in sys.stdin:
                msg += line
        else:
            msg = args.msg
        # msg = "heqwedsaf"

        return {
            'fromaddr': fromaddr,
            'username': username,
            'password': passwd,
            'toaddrs': toaddrs,
            'server': (server, port),
            'data': {'subject': subject, 'msg': msg, 'attach': args.attach},
            'mode': mode,
            'dis_enc': args.dis_enc,
            'debug': args.debug
        }
