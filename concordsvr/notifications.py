import logging, os
import configparser
import smtplib

myDir =(os.path.dirname(os.path.realpath(__file__)))
log = logging.getLogger('notifications')
logFile = os.path.join(myDir,"concord-notifications.log")
logging.basicConfig(format='%(asctime)-15s %(message)s'
                        , level="INFO"
                        ,filename=logFile,
                        filemode='w' )

config = configparser.ConfigParser()
config.read(os.path.join(myDir,"concordsvr.conf"))

def send_the_email(toAddresses, subject, message):
        bSendEmail = config.get("EMAIL","bSendEmail")
        bSendPwd = config.get("EMAIL","bSendPwd")
        send_email( bSendEmail.decode('base64'), bSendPwd.decode('base64'), toAddresses, subject, message)

def send_email(user, pwd, recipient, subject, body):
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server_ssl = smtplib.SMTP_SSL(config.get("email","server"), int(config.get("email","port")))
        server_ssl.ehlo()
        server_ssl.login(gmail_user, gmail_pwd)
        server_ssl.sendmail(FROM, TO, message)
        server_ssl.close()
        log.info("E-mail notification sent")
    except Exception, ex:
        log.error("E-mail notification failed to send: %s" % str(ex))