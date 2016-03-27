# coding=utf-8
from reddit.loginreddit import LoginReddit
from reddit.botinfo import message
#message = True

#TODO display status of Steam API in flair! (Last bot activity: YYYY/MM/DD HH/MM Steam API: Online/Offline)
#TODO make time stamp based on Valve's HQ location (PDT)
#TODO check Steam API every 1 minute or when bot is working
#TODO update flair every minute

#TODO clean up code, more vars, more commenting, more print messages to see status of bot in terminal
#TODO think of a way to display the different threads better

#TODO implement summoning of bot and filtering heroes/game modes
#TODO think of commands to summon bot

#TODO run bot on Raspberry Pi and do stress test

if message: print('[main] importing complete')

if __name__ == "__main__":
    if message: print('[main] loading loginReddit')
    s1 = LoginReddit()
    if message: print('[main] loading loginReddit complete')


