## CRON JOBS:

Any task that you schedule through crons is called a cron job. Cron jobs help us automate our routine tasks, whether they're hourly, daily, monthly, or yearly.

Crontabs use the following flags for adding, listing and removing cron jobs.
* crontab -e: edits crontab entries to add, delete, or edit cron jobs.
* crontab -l: list all the cron jobs for the current user.
* crontab -r: remove the current crontab.
* crontab -ri: remove the current crontab with a Y/N prompt (recommended)

## KEY-TERMS

* cron = system deamon
* cron job = tasks defined to run at given intervals or periods
* crontab = cron job table
* systemctl status cron.service = to check if service is active
* df -h = cmd to see available disk space (-h = human readable)
* chgrp = change the group name of a file or directory

## ASSIGNMENT:

* Create a bash script that writes the current date and time to a file in your home directory
* Register the script in your cron tab so that it runs every minute
* Create a script that writes available disc space to a log file in /var/logs. Use a cron job so that it runs weekly.

## USED RESOURCES:

[crontab-explained](https://devconnected.com/cron-jobs-and-crontab-on-linux-explained/)

[cron_Gurru](https://crontab.guru/)

[freediskspace](https://opensource.com/article/18/7/how-check-free-disk-space-linux)


## DIFFICULTIES:
None

## RESULT:

## Exercise 1:

### Create a bash script that writes the current date and time to a file in your home directory.

![bash-script](../00_includes/Linux/linux8.0.png)

### Register the script in your cron tab so that it runs every minute

![date-script](../00_includes/Linux/linux8.2.png)
![script_exec](../00_includes/Linux/linux8.1.png)

### Create a script that writes available disc space to a log file in /var/logs. Use a cron job so that it runs weekly.
![df-script](../00_includes/Linux/linux8.3.png)

### Register script in crontab scheduled to run weekly on monday at 6 am.
![crontab-diskspace](../00_includes/Linux/linux8.4.png)

### Create log file in /var/log. Adjust the write permissions and change grp to sudo user.
![log-file](../00_includes/Linux/linux8.5.png)

