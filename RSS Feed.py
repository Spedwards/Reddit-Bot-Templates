import feedparser,threading,time,traceback

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
USERAGEN = '''App: RSS Feeds
				Version: %s
				Description: [Do something] with RSS Feeds
				Known Issues: None'''%version # user agent

USERNAME = '' # account username
PASSWORD = '' # account password
SUBREDDT = '' # subreddit

LOOP_DEL = 900 # seconds

FEEDS = [''] # feed url(s)

### /CONFIGURATION ###

def err(tb):
	from datetime import datetime
	d = datetime.now()
	name = 'error{0}.txt'.format(d.strftime('%Y%m%d%H%M%S'))
	f = open(name, 'w')
	tb.print_exc(file=f)
	f.close()

def signIn(username,password,useragent):
	from praw import Reddit
	import re
	r = Reddit(user_agent=re.sub(r'\t+','',useragent))
	r.login(username,password)
	return r
 
def doneList():
	with open('done.txt') as f:
		donelist = f.readlines()
	donelist = [x.strip('\n') for x in donelist]
	return donelist
	
def doneListWrite(content):
	with open('done.txt', 'a') as f:
		f.write(content)

r = signIn(USERNAME,PASSWORD,USERAGEN)
subreddit = r.get_subreddit(SUBREDDT)

while looping:
	try:
		already_done = doneList()
		for feed in FEEDS:
			f = feedparser.parse(feed)
			for item in f['entries']:
				guid = item.guid
				if guid not in already_done:
					# Do something
					doneListWrite('%s\n'%guid)
	except Exception as e:
		err(traceback)
	time.sleep(LOOP_DEL)
