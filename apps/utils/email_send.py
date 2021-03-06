# -*- coding: utf-8 -*-
from random import Random
from users.models import EmailVerifyRecode
from django.core.mail import send_mail
from django_xadmin.settings import EMAIL_FROM


def random_str(randomlength=8):
    str = ''
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecode()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''
    if send_type == 'register':
        email_title = 'django在线学习网注册激活链接'
        email_body = '请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{}'.format(code)

        send_status =False
        try:
            send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        except Exception as e:
            print e

        if send_status:
            print 'into send_status'
    elif send_type == 'forget':
        email_title = 'django在线学习网重新找回密码'
        email_body = '请点击下面的链接重新找回账户密码: http://127.0.0.1:8000/reset/'

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
