import zmail


def sEmail(rPath, sendEmail):

    reportPath = rPath
    with open(reportPath, 'r', encoding='utf-8') as f:
        content_html = f.read()
    mail = {
        'subject': 'Success!',  # Anything you want.
        'content_html': content_html,
        'attachments': reportPath,  # Absolute path will be better.
    }
    server = zmail.server('1187338689@qq.com', 'zqkdugheciyxbagj')
    server.send_mail(sendEmail, mail)
    return