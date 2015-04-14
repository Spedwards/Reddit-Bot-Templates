import re,threading,time

def basicThread():
	global looping
	looping = True
	while True:
		i = input()
		if i == 'exit':
			looping = False
			print('Loop will close on next iteration.')
		else:
			print('>>', i)

t1 = threading.Thread(target=basicThread)
t1.daemon = True
t1.start()

###  CONFIGURATION ###

version = '1.0.0' # bot version
USERAGEN = '''App: Sidebar
				Version: %s
				Description: Update subreddit sidebar
				Known Issues: None'''%version # user agent

USERNAME = '' # account username
PASSWORD = '' # account password
SUBREDDT = '' # subreddit

SIDEBAR = '''Your subreddit content.
			
			Add values you want dynamic in curly parenthesis.  
			{example}
			
			That example can be set to whatever you like.'''

LOOP_DEL = 300 # seconds

### /CONFIGURATION ###

SIDEBAR = re.sub(r'\t+','',SIDEBAR)

def signIn(username,password,useragent):
	import praw
	import re
	r = praw.Reddit(user_agent=re.compile(r'\t+').sub('',useragent))
	r.login(username,password)
	return r

r = signIn(USERNAME,PASSWORD,USERAGEN)
subreddit = r.get_subreddit(SUBREDDT)

while looping:
	subreddit.update_settings(description=SIDEBAR.format(
		example='whatever the hell you like'
	))
	time.sleep(LOOP_DEL)
