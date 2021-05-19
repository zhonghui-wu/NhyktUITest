import zmail


def sEmail(rPath, sendEmail):

    reportPath = rPath
    with open(reportPath, 'r', encoding='utf-8') as f:
        content_html = f.read()
    mail = {
        'subject': '南海云课堂管理后台自动化测试报告',  # Anything you want.
        'content_html': content_html,
        'attachments': reportPath,  # Absolute path will be better.
    }
    # 发送 企业邮箱
    server = zmail.server('rock.wu@cloudcall.hk', 'r6jDT9b2snY9C3Jp', smtp_host='smtp.exmail.qq.com', smtp_port=465)
    # 发送 qq 邮箱
    # server = zmail.server('1187338689@qq.com', 'zqkdugheciyxbagj')
    server.send_mail(sendEmail, mail)
    return


# sEmail('./report.html', 'doreen.deng@cloudcall.hk')