def isPrime(number):
	#Return true for prime number
	if number<0:
		return False
	if number%2==0:
		return number==2
	d=3
	while d*d<=number and number%d!=0:
		d+=2
	return d*d>number