import datetime as dt

class pynvg:
	def __init__(self):
		print("Hello pynvg")

def dolog(text,filename=None):
	#Makes log file
	if filename is None:
		filename="nvglog-"+dt.datetime.now().strftime("%m_%d_%Y__%H_%M_%S")+".txt"

	try:
		with open(filename,"r") as f:
			temp=f.read()
	except:
		temp=""

	with open(filename,"w") as f:
		f.write("["+dt.datetime.now().strftime("%m_%d_%Y__%H_%M_%S")+"]: "+str(text)+"\n"+temp)