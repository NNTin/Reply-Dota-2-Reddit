import time
from reddit.botinfo import botName
from reddit.redditconstants import MAXPOSTS, WAIT
from reddit.redditconstants import PRIVILEDGEDAUTHORS
#message = True


def deleteRequestedComments(r):
    print(botName)

    while True:
        try:
            print('[workerdeleterequestedcomments] checking mail with DELETION subject')
            unread = r.get_unread(limit=MAXPOSTS)
            for msg in unread:
                try:
                    print('mail found')
                    if (msg.subject == 'deletion'):
                        print('subject deletion')
                        comment = r.get_info(thing_id=msg.body)
                        print('forming comment success')
                        commentParent = r.get_info(thing_id=comment.parent_id)
                        print('getting parent success')
                        if (msg.author.name in PRIVILEDGEDAUTHORS or msg.author.name == commentParent.author.name):
                            print('found to be deleted comment')
                            comment.delete()
                            print('deleting comment')
                        msg.mark_as_read()
                        print('mark as read')
                except:
                    print('Fail?')
            time.sleep(3*WAIT)
        except:
            time.sleep(3*WAIT)


