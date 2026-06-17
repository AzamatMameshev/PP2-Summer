# 1 Subtract 5 days

from datetime import datetime, timedelta

now = datetime.now()
print(now - timedelta(days=5))     

# 2. Yesterday, Today, Tomorrow

from datetime import date, timedelta

today = date.today()
print(today - timedelta(days=1))
print(today)            
print(today + timedelta(days=1))

# 3 Drop microseconds

from datetime import datetime

dt = datetime.now()     
print(dt.replace(microsecond=0))

# 4. Difference in seconds
from datetime import datetime  

d1 = datetime(2024, 1, 1)
d2 = datetime(2024, 1, 10)

print((d2 - d1).total_seconds()) 