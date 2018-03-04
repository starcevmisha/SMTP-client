import base64
import os


class Email:

    def __init__(self, fromaddr, toaddrs, subject, message,
                 attachments=None):
        self.boundary = "--===============8484777675788374285=="
        self.email = 'Content-Type: multipart/mixed; boundary="{}"\r\n' \
            .format(self.boundary[2:])
        self.email += "MIME-Version: 1.0\r\n"

        self.email += "From: {}\r\n".format(fromaddr)
        self.email += "Subject: {}\r\n".format(subject)
        self.email += "To: {}\r\n\r\n".format(",".join(toaddrs)
                                              if isinstance(toaddrs, list)
                                              else toaddrs)

        self.email += self.boundary + "\r\n"
        self.email += 'Content-Type: text/plain; charset="utf-8"\r\n' \
                      'MIME-Version: 1.0\r\n' \
                      'Content-Transfer-Encoding: 8bit\r\n\r\n'

        self.email += "{}\r\n".format(message)

        if attachments is not None:
            for file in attachments:
                name, alias = get_name(file)
                attach = self.boundary
                attach += '\r\nContent-Type: application/octet-stream; ' \
                          'Name="{0}"\r\n' \
                          'MIME-Version: 1.0\r\n' \
                          'Content-Transfer-Encoding: base64' \
                          '\r\nContent-Disposition: attachment; ' \
                          'filename="{0}"\r\n\r\n'.format(alias)

                with open(name, 'rb') as f:
                    a = f.read()
                    a = base64.b64encode(a)
                    # print(a)
                    attach += a.decode('ascii')
                    self.email += attach + '\r\n\r\n'

        self.email += self.boundary + "--"


def get_name(filename):
    f = tuple(filename.rsplit(':', 1))
    return f[0], f[1] if len(f) > 1 else os.path.basename(f[0])
