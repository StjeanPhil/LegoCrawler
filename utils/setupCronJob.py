import random
import subprocess

# Generate random hours for the two executions
minute = random.randint(0, 59)
hour = random.randint(0, 12)
minute2 = random.randint(0, 59)
hour2 = random.randint(hour+5, 23)

# Format the cron schedule strings
cron_schedule1 = f"{minute} {hour} * * * /usr/bin/python /LegoCrawler/bot/MainCrawl.py"
cron_schedule2 = f"{minute2} {hour2} * * * /usr/bin/python /LegoCrawler/bot/MainCrawl.py"

reshedule = f" 0 0 * * * /usr/bin/python /LegoCrawler/utils/setupCronJob.py"

#delete the old cron job
subprocess.run(["crontab", "-r"])

# Update the cron job
with open("/tmp/crontab.txt", "w") as file:
    file.write(f"{cron_schedule1}\n{cron_schedule2}\n")

# Load the new cron job
subprocess.run(["crontab", "/tmp/crontab.txt"])