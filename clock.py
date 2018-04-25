"""
Run the background scheduler to schedule a job
"""

from datetime import datetime
import time
import os
if not os.environ.get("DJANGO_SETTINGS_MODULE"):
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todo.settings")

from apscheduler.schedulers.background import BackgroundScheduler

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

sched = BackgroundScheduler()


@sched.scheduled_job('interval', minutes=2)
def tick():
    from todoapp.views import permannat_delete_task
    print('Tick Running. The time is: %s' % datetime.now())
    permannat_delete_task()

if __name__ == '__main__':
    # to start schedulers you need to run "python clock.py"
    sched.start()
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        # while True:
        #     time.sleep(0.5)
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        sched.shutdown()