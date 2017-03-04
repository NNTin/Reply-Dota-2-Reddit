import time
from reddit.redditconstants import MAXPOSTS, WAIT
from reddit.redditconstants import PRIVILEDGEDAUTHORS
#message = True


def deleteRequestedComments(r):
    while True:
        try:
            print('[workerdeleterequestedcomments] checking mail with DELETION subject')
            unread = r.inbox.unread()
            for msg in unread:
                print('You have Mail!')
                try:
                    if (msg.subject == 'deletion'):
                        print('subject deletion')
                        genComment = r.info([msg.body])
                        comment = next(genComment)
                        print('forming comment success')
                        commentParent = comment.parent()
                        print('getting parent success')

                        if (msg.author.name in PRIVILEDGEDAUTHORS or msg.author.name == commentParent.author.name):
                            print('found to be deleted comment')
                            comment.delete()
                            print('deleting comment')

                        print('mark as read')
                except:
                    print('Fail?')
                msg.mark_read()
            time.sleep(3*WAIT)
        except:
            print('[workerdeleterequestedcomments] Crashed')
            time.sleep(3*WAIT)


