import datetime
import pytz

# using now() to get current time
current_time = datetime.datetime.now() - datetime.timedelta(hours=1)

# Printing value of now.
print(f"{current_time:%d/%m/%Y %H:%M}")
