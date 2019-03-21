import praw
from bot import Chatter_Stats_Bot

clientId = '' #Insert client ID
clientSecret = '' #Insert client secret
username = '' #Insert reddit username
password = '' #Insert reddit password
imgurClientID = ''
imgurClientSecret = ''

r = praw.Reddit(client_id=clientId, client_secret=clientSecret, password=password, user_agent='Updating game thread',
                username=username)

CSB = Chatter_Stats_Bot(r, imgurClientID)
CSB.run()
