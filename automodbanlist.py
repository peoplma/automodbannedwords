import time
import praw
import sys
import traceback

subName = set(['btc'])
r = praw.Reddit('automodbanlistchecker')
r.login("username1","password")
reddit = praw.Reddit('automodbanlist')
reddit.login("username2","password")
already_done = set()
words = []
commentset = set()
threadcomments = set()

for n in subName:
	subreddit = reddit.get_subreddit(n)
	for comment in subreddit.get_comments(limit=1000):
		if not comment.author:
			continue
		else:
			if comment.id not in already_done:
				commentset = comment.body.lower().split()
				already_done.add(comment.id)
				for item in commentset:
					if item not in words:
						words.append(item)
					else:
						continue
			else:
				continue
	print(words)
	print(len(words))

def main(subName):
	submission = reddit.get_submission(submission_id='5v7ix9')	
	for i in words:
		try:
			print(str(i)+" - commenting word")
		except:
			continue
		testperma = submission.add_comment(i)
		time.sleep(30)
		commentcheck = r.get_submission(submission_id='5v7ix9')
		commentcheck.replace_more_comments(limit=None, threshold=0)
		for comment in commentcheck.comments:
			threadcomments.add(comment.body)
		print(threadcomments)
		if i not in threadcomments:
			try:
				print(str(i)+' not found in comments, adding to list')
			except:
				continue
			listed = open('list.txt', 'ab+')
			listed.write(str(i)+', ')
			listed.close()
		testperma.delete()
		threadcomments.clear()
		words.remove(i)
		print(len(words))

def secondary():
	try:
		while True:
			main(subName)
	except:
		traceback.print_exc()
		print('Resuming in 2sec...')
		time.sleep(2)
		
while True:
	secondary()
