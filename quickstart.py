from instapy import InstaPy
#insta_username = 'explore.motherfucker'
#insta_password = '321592230z'

insta_username = 'dankestt_of_memes'
insta_password = 'bullseye10'

BASE_FOLLOWS = 0.81
BASE_LIKES = 0.46


# set headless_browser=True if you want to run InstaPy on a server
try:
    session = InstaPy(username=insta_username,
                      password=insta_password,
                      headless_browser=True,
                      multi_logs=True,
		      bypass_suspicious_attempt=True)
    session.login()
    fph = 120
    session.set_sleep_reduce(100*fph/(BASE_FOLLOWS*60))
    # actions
    session.interact_user_commenters2(['fuckjerry', 'thetastelessgentlemen', 'daquan'], amount_of_follows=50)


finally:
    # end the bot session
    session.end()
