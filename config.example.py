# save this file as config.py

bot_token = 'insert_token'
bot_channel = 'channel_id'
bot_prefix = '!'

# replace devicename and uuid for each device
devices={'devicename1':'uuid1',
    'devicename2':'uuid2',
    'devicename3':'uuid3'
    }
    
#    
app_alias={'app1':'app.bundle.identifier',
    'app2':'app2.bundle.identifier'

    }

# Optional MYSQL Database Settings.
# if DB_USER = 'user' and DB_PASSWORD = 'ABCD1234' MySQL functionality is off.
DB_NAME = 'db'

DB_HOST = 'port9000'

DB_USER = 'user'

DB_PASSWORD = 'abcd1234'

# srSQl1 will run a conitnuous background task. query_interval in seconds.
query_interval = 120
strSQL1 = ("SELECT * FROM tblname")

# strSQL2 works with query command. you can define multiple queries to run on demand. syntax !query strSQL2

strSQL2 = ''
