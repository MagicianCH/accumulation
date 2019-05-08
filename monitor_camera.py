import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from picamera import PiCamera
from time import sleep

class SendMail(object):
    def __init__(self):
        self.host_server = "smtp.163.com"
        self.sender_addr = "chenhao1737@163.com"
        self.sender_pwd = "xxxxx"
        self.receiver_addr = "chenhao_ustb@163.com"
        self.mail_msg = MIMEMultipart()

    def configure(self, title):
        self.mail_msg["Subject"] = Header(title, 'utf-8')
        self.mail_msg["From"] = self.sender_addr
        self.mail_msg["To"] = Header("chenhao_ustb@163.com", 'utf-8') ## 接收者的别名
        self.mail_msg.attach(MIMEText("photo", 'html', 'utf-8'))

    def add_attatchment(self, att, name):
        self.attatchment = MIMEText(open(att, 'rb').read(), 'base64', 'utf-8')
        self.attatchment["Content-Type"] = 'application/octet-stream'
        self.attatchment["Content-Disposition"] = 'attachment; filename=name'
        self.mail_msg.attach(self.attatchment)

    def send(self):
        smtp = smtplib.SMTP_SSL(self.host_server)
        smtp.set_debuglevel(1)
        smtp.ehlo(self.host_server)
        smtp.login(self.sender_addr, self.sender_pwd)
        smtp.sendmail(self.sender_addr, self.receiver_addr, self.mail_msg.as_string())
        smtp.quit()

class MyCamera(object):
    def __init__(self):
        self.camera = PiCamera()
        
    def take_picture(self, name):
        self.camera.start_preview()
        sleep(5)
        self.camera.capture(name)
        self.camera.stop_preview()

if __name__ == '__main__':
    cam = MyCamera()
    mail = SendMail()
    mail.configure('photo')
    num = 0
    while True:
        try:
            num += 1
            img_name = 'images/image%s.jpg'%num
            cam.take_picture(img_name)
            mail.add_attatchment(img_name, img_name)
            mail.send()
            sleep(1800)
        except Exception as e:
            print(e)
            print("stop!")
