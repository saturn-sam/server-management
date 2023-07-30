import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SendMail():
	def __init__(self):
		self.sender = "samrat.ict@pubalibankbd.com"
		# self.senderPassword = 
		self.server = smtplib.SMTP('172.16.254.3')
		# self.server.ehlo()
		# self.server.starttls()
		# self.server.login(self.sender, self.senderPassword)

	# Order of parameters matter
	def send(self, reciever, subject, message):
		msg = MIMEMultipart()
		msg['From'] = self.sender
		msg['To'] = reciever
		msg['subject'] = subject
		Message = message
		msg.attach(MIMEText(Message, 'plain'))
		text = msg.as_string()
		self.server.sendmail(self.sender, reciever, text)
		return