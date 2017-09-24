@StarcevMichail 2017


SMTP Implementation

General description

This is smtp protocol implementation

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        SMTP server
  -f FROMADDR, --fromaddr FROMADDR
                        From address
  -p PASSWD, --passwd PASSWD
                        Password for login
  -t, [TOADDRS [TOADDRS ...]], --toaddrs [TOADDRS [TOADDRS ...]]
                        To addresses
  --subj SUBJ           Subject of the message
  -m MSG, --msg MSG     Message for recipients
  -a [ATTACH [ATTACH ...]], --attach [ATTACH [ATTACH ...]]
                        Attachments for email. You can rename yor files using this construction
                        -a old_name:new_name
  --mode {separate,together,group}
                        Distribution mode
  --dis-enc             disable encryption
  --debug               Debug Mode



Example:
smtp_console.py --server smtp.gmail.com:465 --fromaddr smtp.task3@gmail.com --passwd pythonpython --toaddrs starcev_misha@mail.ru --subj TestSmtpClient --msg iloveyouPython  --attach 123.txt 12.png samokat.png --mode together