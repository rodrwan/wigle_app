#!/usr/bin/python
#
# Forma de ejecutar el programa
# python wigle_v3.py ssid netid
#
# programa entrega direccion aproximada de longitud y latitud
import sys
import urllib2
import urllib
import cookielib
import json

cj = cookielib.CookieJar()

if len(sys.argv)<2:
	print "Faltaron parametros, recuerde python wigle.py ssid netid"
	sys.exit(2)

username = 'user_wigle'
password = 'pass_wigle'

ssid = sys.argv[1] # ssid a buscar
netid = sys.argv[2] # net id a buscar

host = 'https://wigle.net/'

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

login_data = urllib.urlencode({
	'credential_0': username, 
	'credential_1' : password , 
	'destination':'/gps/gps/main/query/', 
	'noexpire' : '1' })	

opener.open(host + 'gps/gps/main/login/', login_data)

uri = '?addresscode=&citycode=&statecode=&zipcode=&variance=0.010&ssid='+ssid+'&netid='+netid

output = (opener.open(host + 'gps/gps/main/confirmquery/' + uri )).read()

a = output.index('<a href="/gps/gps/Map/onlinemap2/?maplat=')+10
uri = output[a:output.index('">Get Map</a>', a)]


dict_uri = {}
uri_split = uri.split("?")
next_split = uri_split[1].split("&")
for i in next_split:
	final_split = i.split("=")
	if final_split[0] == 'maplon':
		dict_uri['longitud'] = final_split[1]
	elif final_split[0] == 'maplat':
		dict_uri['latitud'] = final_split[1]
	else:
		dict_uri[final_split[0]] = final_split[1]
	if final_split[0] == 'mapzoom':
		del dict_uri['mapzoom']
j = json.dumps(dict_uri, sort_keys=True, indent=4)

l = json.loads(j)

jason = (opener.open("http://maps.google.com/maps/api/geocode/json?latlng=" + l['latitud'] + "," + l['longitud'] + "&sensor=false")).read()

l = json.loads(jason)

print l['results'][0]['formatted_address']
print l['results'][1]['formatted_address']