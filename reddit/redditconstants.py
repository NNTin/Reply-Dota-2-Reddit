SUBREDDIT = "Lumbdi"
# This is the sub or list of subs to scan for new posts. For a single sub, use "sub1". For multiple subreddits, use "sub1+sub2+sub3+..."
KEYWORDS = ["dotabuff.com/players/", "yasp.co/players/"]
# These are the words you are looking for
# Ignore these authors
MAXPOSTS = 100
# This is how many posts you want to retrieve all at once. PRAW can download 100 at a time.
WAIT = 10
# This is how many seconds you will wait between cycles. The bot is completely inactive during this time.
CLEANCYCLES = 10
# After this many cycles, the bot will clean its database
# Keeping only the latest (2*MAXPOSTS) items

#https://www.reddit.com/user/AnalyzeLast100Games