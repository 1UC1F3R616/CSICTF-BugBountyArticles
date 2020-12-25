import os
from time import sleep

# SECRETS
WEB_HOOK = os.getenv('WEB_HOOK')
CHAT_ID = "CSICTF"

# scraper import
from scrapes.bug_bytes import result as bug_bytes_result
from scrapes.portswigger_research import result as portswigger_research_result
from scrapes.pentester_land import result as pentester_land_result

# scraper run
def run_bot(event, context):
    bug_bytes_result(WEB_HOOK=WEB_HOOK, CHAT_ID=CHAT_ID)
    portswigger_research_result(WEB_HOOK=WEB_HOOK, CHAT_ID=CHAT_ID)
    pentester_land_result(WEB_HOOK=WEB_HOOK, CHAT_ID=CHAT_ID)
    print('bot ran successfully')
    return {
        'statusCode': 200
    }
