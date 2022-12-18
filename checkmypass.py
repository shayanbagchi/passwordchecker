import requests
import hashlib
import sys

def req_api_data(query):
	url = 'https://api.pwnedpasswords.com/range/' + query
	res = requests.get(url)
	if res.status_code != 200:
		raise RuntimeError(f'Error: {res.status_code}')
	return res

def get_pass_leak_count(hashlst, hash_to_check):
	hashes = (line.split(':') for line in hashlst.text.splitlines())
	for h, count in hashes:
		if h == hash_to_check:
			return count
	return 0 
	

def pwned_api_check(password):
	sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	first_5_char, tail = sha1password[:5], sha1password[5:]
	res = req_api_data(first_5_char)
	return(get_pass_leak_count(res, tail))

def main(args):
	for password in args:
		count = pwned_api_check(password)
		if count:
			print(f"Your password - {password} is pwned {count} times. Change it ASAP!\n")
		else:
			print(f"Your password - {password} is a safe one. Carry Onn!\n")
	return 'Done!'


if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))