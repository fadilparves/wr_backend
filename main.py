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
                            start="May 23 12:00:00 2022",
                            tz="Asia/Kuala_Lumpur",
                            kwargs={"tf":'1min', "stf": "1m", "ttf": 'Trend_1M'})

recurring_scheduler.add_job(target=update_ms,
                            period_in_seconds=300,
                            start="May 23 12:05:00 2022",
                            tz="Asia/Kuala_Lumpur",
                            kwargs={"tf":'5min', "stf": "5m", "ttf": 'Trend_5M'})

recurring_scheduler.add_job(target=update_ms,
                            period_in_seconds=900,
                            start="May 23 12:15:00 2022",
                            tz="Asia/Kuala_Lumpur",
                            kwargs={"tf":'15min', "stf": "15m", "ttf": 'Trend_15M'})

recurring_scheduler.add_job(target=update_ms,
                            period_in_seconds=3600,
                            start="May 23 13:00:00 2022",
                            tz="Asia/Kuala_Lumpur",
                            kwargs={"tf":'60min', "stf": "1h", "ttf": 'Trend_H1'})

recurring_scheduler.add_job(target=update_ms,
                            period_in_seconds=14400,
                            start="May 23 16:00:00 2022",
                            tz="Asia/Kuala_Lumpur",
                            kwargs={"tf":'4hour', "stf": "4h", "ttf": 'Trend_4H'})

recurring_scheduler.add_job(target=update_ms,
                            period_in_seconds=86400,
                            start="May 24 00:00:00 2022",
                            tz="Asia/Kuala_Lumpur",
                            kwargs={"tf":'1day', "stf": "1d", "ttf": 'Trend_1D'})

recurring_scheduler.add_job(target=crypto_info,
                            period_in_seconds=2628000,
                            start="June 01 00:00:00 2022",
                            tz="Asia/Kuala_Lumpur")

recurring_scheduler.add_job(target=shariah_status,
                            period_in_seconds=2628000,
                            start="June 01 00:05:00 2022",
                            tz="Asia/Kuala_Lumpur")

recurring_scheduler.run()