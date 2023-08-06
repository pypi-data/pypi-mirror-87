from datetime import datetime

def log(message):
	print(datetime.now().strftime("%m/%d/%Y %H:%M:%S"), message)
