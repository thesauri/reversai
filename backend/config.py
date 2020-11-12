from dotenv import load_dotenv

try:
  load_dotenv('../.env')
except:
  print('Could not load .env file. This is probably OK, unless your name is Samuel')
