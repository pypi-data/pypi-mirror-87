def abool(var):
	#Converts true/false to 1/-1 system (Positive/Negative)
    if(var):	return 1
    else:  	return -1

def bitvector(val,total=2):
	#Returns a vector with zeros and only one where necessary
	return [1 if i==val else 0 for i in range(total)]