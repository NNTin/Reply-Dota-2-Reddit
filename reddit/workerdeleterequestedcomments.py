import time
from reddit.redditconstants import MAXPOSTS, WAIT
from reddit.redditconstants import PRIVILEDGEDAUTHORS
#message = True


def deleteRequestedComments(r):
    while True:
        try:
            print('[workerdeleterequestedcomments] checking mail with DELETION subject')
            unread = r.get_unread(limit=MAXPOSTS)
            for msg in unread:
                print('You have Mail!')
                try:
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

                        print('mark as read')
                except:
                    print('Fail?')
                msg.mark_as_read()
            time.sleep(3*WAIT)
        except:
            print('[workerdeleterequestedcomments] Crashed')
            time.sleep(3*WAIT)


