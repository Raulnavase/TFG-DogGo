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

def send_reset_email(to_email, token):
    remitente = getenv("REMITENTE_EMAIL")
    password = getenv("PASSWORD_EMAIL")
    asunto = "Recupera tu contraseña en DogGo"
    enlace = "https://tfg-dog-go.vercel.app/reset-password/{}".format(token)
    cuerpo = "Hola,\n\nHaz clic en el siguiente enlace para restablecer tu contraseña:\n{}\n\nSi no solicitaste este cambio, ignora este correo.".format(enlace)
    msg = MIMEText(cuerpo)
    msg['Subject'] = asunto
    msg['From'] = remitente
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(remitente, password)
        server.sendmail(remitente, to_email, msg.as_string())