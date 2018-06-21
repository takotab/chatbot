import requests
import json
import sys

def getpostcode(housenumber, postcode):
	url = "https://api.postcodeapi.nu/v2/addresses/"
	querystring = {"postcode":postcode,"number":housenumber}
	headers = {
		'x-api-key': "TJYq7kMV324WPS0JwhZLz87iXsIc79mQ7gxJgr3x",
		'accept': "application/hal+json"
	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	urlResponse = response.text
	print
	items = json.loads(urlResponse)
	errorCheck = items.get('error', 'null')
	if(errorCheck == 'null'):	
		addresslength = len(items['_embedded']['addresses'])
		if(addresslength > 1):
			return "multiple"
		elif (addresslength == 1):
			addressdetails = items['_embedded']['addresses'][0]
			municipality = '';
			if(addressdetails.get('municipality', 'null') != 'null'):
				municipality = addressdetails['municipality'].get('label', '')
				municipality=municipality.encode("ascii","replace")
			street = addressdetails.get('street', '')
			if(street !='null'):
				street = street.encode("ascii","replace")			
			province = ''
			if(addressdetails.get('province', 'null') != 'null'):
				province = addressdetails['province'].get('label', '')
				province=province.encode("ascii","replace")					
			return street,municipality,province
		else:
			return "error"
	else:
		return "error"

#housenumber = sys.argv[1]
#postcode = sys.argv[2]

#print (getpostcode(2,"2408HK"))
	
