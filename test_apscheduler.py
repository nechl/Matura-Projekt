from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def my_job(test):
    print(test)
    
scheduler.add_job(my_job, 'date', run_date=datetime(2021, 9, 13, 17, 43, 30), args=["it works"], id='my_job_id')
scheduler.start()

while True:
    pass