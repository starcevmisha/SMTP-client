import re
from SMTP_pack.argumentsForConfig import Arguments
from SMTP_pack.smtp_server import SMTP

from SMTP_pack.email_format import Email



def send_mail(toaddr, args):
    mail = Email(fromaddr=args["fromaddr"], toaddrs=toaddr,
                 subject=args['data']['subject'], message=args['data']['msg'],
                 attachments=args['data']['attach'])
    error = client.sendMail(toaddr, mail.email)
    if len(error) > 0:
        print('mail not recived to:{}'.format(', '.join(error)))


if __name__ == '__main__':

    parser = Arguments()
    args = parser.get_args("ToSend/config.txt")

    client = SMTP(args['debug'])
    client.open_connection(args['server'], args['dis_enc'])
    client.helo()
    client.auth(args['username'], args['password'])

    if args['mode'] == 'together':
        send_mail(args["toaddrs"], args)

    elif args['mode'] == 'separate':

        for addr in args["toaddrs"]:
            send_mail(addr, args)

    elif args['mode'] == 'group':
        print(" ".join(args["toaddrs"]))
        reg = re.compile(r'\(([.\w@+\ +]+)\)')
        groups = reg.findall(" ".join(args["toaddrs"]))
        print(groups)
        for group in groups:
            group = group.split(' ')
            send_mail(group, args)

    client.close()
