#!\urs\bin\env python  
#encoding: utf-8  
import web  
      
def send_mail(send_to, subject, body):
    ''''' 
    @把找回密码的内容作为邮件发送出去 
    '''  
    try:
        web.config.smtp_server = 'smtp.qq.com'   ##邮件发送服务器  
        web.config.smtp_port = 25    ##不设置将使用默认端口  
        web.config.smtp_username = '824010343@qq.com'   ##邮件服务器的登录名
        web.config.smtp_password = 'trthwhhcqwxebgab'   ##邮件服务器的授权码
        web.config.smtp_starttls = True  
        send_from = '824010343@qq.com'    ##发送的邮件
        web.sendmail(send_from, send_to, subject, body)
        return 1  #pass  
    except Exception, e:  
        print e  
        return -1 #fail  
'''
if __name__=='__main__':
    send_to = ['824010343@qq.com']
    subject = '欢迎注册  Oletter '
    body = '请点击以下链接\n'
    #cc = ['824010343@qq.com', 'someone2@sina.com']   ##抄送
    #bcc = ['824010343@qq.com', 'someone2@sina.com']  ##密抄
    send_mail(send_to, subject, body)
'''