#SUBREDDIT = "Lumbdi"
SUBREDDIT = "AnalyzeLast100Games+Dota2"
# This is the sub or list of subs to scan for new posts. For a single sub, use "sub1". For multiple subreddits, use "sub1+sub2+sub3+..."
KEYWORDS = ["dotabuff.com/players/", "yasp.co/players/", "opendota.com/players/", "dotabuff.com/matches/", "yasp.co/matches/", "opendota.com/matches/"]
# These are the words you are looking for
IGNOREAUTHORS = ["dotamatch", "AnalyzeLast100Games", "Lumbditest"]
# Ignore these authors fdsfjkl
PRIVILEDGEDAUTHORS = ['ReaverXai', 'm4rx', 'klopjobacid', 'Decency', '0Hellspawn0', 'wykrhm', 'crimson589',
                      'Intolerable', 'lestye', 'intolerable-bot', 'D2TournamentThreads', 'AutoModerator',
                      'coronaria', 'leafeator', 'lumbdi']
# These authors can force the bot to delete his own comments
MAXPOSTS = 100
# This is how many posts you want to retrieve all at once. PRAW can download 100 at a time.
WAIT = 10
# After this many cycles, the bot will clean its database
# Keeping only the latest (2*MAXPOSTS) items

#https://www.reddit.com/user/AnalyzeLast100Games