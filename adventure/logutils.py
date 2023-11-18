import datetime

timestamp_logfile = f"logs/debug-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log"
default_logfile = f"logs/debug-current.log"

def log(text):
    with open(timestamp_logfile, 'a') as timestamp_log, open(default_logfile, 'a') as default_log:
        timestamp_log.write(f"{text}\n")
        default_log.write(f"{text}\n")
