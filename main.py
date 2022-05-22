from scheduler.recurring import recurring_scheduler
from simple_scheduler.event import event_scheduler
from datetime import datetime
from pytz import all_timezones, timezone
from crypto_info import crypto_info
from shariah_info import shariah_status

print("Scheduler Started")

recurring_scheduler.add_job(target=crypto_info,
                            period_in_seconds=60,
                            start="May 22 22:06:00 2022",
                            tz="Asia/Kuala_Lumpur")

event_scheduler.add_job(target=crypto_info,
                        when = ["mon|8:00"] ,
                        tz = "Asia/Kuala_Lumpur",
                        start="May 24 08:00:00 2022")

event_scheduler.add_job(target=shariah_status,
                        when = ["mon|9:00"] ,
                        tz = "Asia/Kuala_Lumpur",
                        start="May 24 08:00:00 2022")

event_scheduler.run()
recurring_scheduler.run()