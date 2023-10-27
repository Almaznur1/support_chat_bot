from os import getenv
from dotenv import load_dotenv


load_dotenv()
tg_bot_token = getenv('TG_BOT_TOKEN')
project_id = getenv('PROJECT_ID')
language_code = getenv('LANGUAGE_CODE')
