import praw
import OAuth2Util
import time
from reddit import botinfo
from reddit.redditconstants import PRIVILEDGEDAUTHORS


while True:
    r = praw.Reddit(botinfo.app_ua)
    o = OAuth2Util.OAuth2Util(r)
    o.refresh(force=True)

    subreddit = r.get_subreddit('Lumbdi')
    posts = list(subreddit.get_comments(limit=100))

    #posts.reverse()

    my_new_comment = posts[0].reply('[^^source](http://github.com/NNTin/Reply-Dota-2-Reddit) ^^on ^^github, [^^summon](https://www.reddit.com/r/DotA2/comments/4cl7cl/uanalyzelast100games_now_supports_filtering_by/ "<player link> [amount:<amount of games>] [view:detailed] [heroes:<hero name>{+<hero name>}]") ^^the ^^bot')
    message_template = 'https://www.reddit.com/message/compose/?to=' + botinfo.botName + '&subject=deletion&message={fullname}'
    delete_link = message_template.format(fullname=my_new_comment.fullname)

    footer_template = ', [^^deletion ^^link]({url} "Only works for bot summoner and /r/dota2 mods! Do not change content!")'
    footer = footer_template.format(url=delete_link)
    my_new_comment.edit(my_new_comment.body + footer)

    while True:
        print('checking mail')
        unread = r.get_unread(limit=100)
        for msg in unread:
            if (msg.subject == 'deletion'):
                print('deletion comment found!')

                print('author: %s text: %s' %(msg.author.name, msg.body))

                print(msg.subject)

                comment = r.get_info(thing_id=msg.body)
                print('Comment was written by: %s' %comment.author.name)
                time.sleep(5)
                commentParent = r.get_info(thing_id=comment.parent_id)
                print('Parent Comment was written by: %s' %commentParent.author.name)

                print('jfkjsdlkf' + commentParent.author.name)

                priviledgedAuthors = []
                for author in PRIVILEDGEDAUTHORS:
                    priviledgedAuthors.append(author)
                priviledgedAuthors.append(commentParent.author.name)

                if (msg.author.name in priviledgedAuthors):
                    print('this guy is allowed to delete the comment!')
                    comment.delete()
                    print('deleted')



                msg.mark_as_read()


        time.sleep(5)



