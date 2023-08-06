import requests

def nvgli(url):
	URL_shortening_service="https://nvg.li/php/a/shorturl.php?url="
	query=r.post(URL_shortening_service+url)
	if query.status_code==200:
		return query.text
	else:
		return False