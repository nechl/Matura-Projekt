from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def my_job(test):
    print(test)
    
scheduler.add_job(my_job, 'date', run_date=start_at, args=["it works"], id='my_job_id')
scheduler.start()

while True:
    pass