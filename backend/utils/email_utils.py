import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from os import getenv

load_dotenv()

def send_welcome_email(to_email, name):
    remitente = getenv("REMITENTE_EMAIL")
    password = getenv("PASSWORD_EMAIL")
    asunto = "¡Bienvenido a DogGo!"
    cuerpo = "Hola {},\n\n¡Gracias por registrarte en DogGo! Esperamos que disfrutes de la experiencia.\n\nEl equipo de DogGo".format(name.capitalize())

    msg = MIMEText(cuerpo)
    msg['Subject'] = asunto
    msg['From'] = remitente
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(remitente, password)
        server.sendmail(remitente, to_email, msg.as_string())