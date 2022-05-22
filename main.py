from scheduler.recurring import recurring_scheduler
from scheduler.event import event_scheduler
from datetime import datetime
from pytz import all_timezones, timezone
from crypto_info import crypto_info
from shariah_info import shariah_status
from ms_update import update_ms

print("Scheduler Started")

recurring_scheduler.add_job(target=update_ms,
                            period_in_seconds=60,
                            start="May 22 22:37:00 2022",
                            tz="Asia/Kuala_Lumpur",
                            kwargs={"tf":'1min', "stf": "1m", "ttf": 'Trend_1M'})

# recurring_scheduler.add_job(target=update_ms,
#                             period_in_seconds=60,
#                             start="May 22 22:06:00 2022",
#                             tz="Asia/Kuala_Lumpur",
#                             kwargs={"tf":'1min', "stf": "1m"})

recurring_scheduler.run()