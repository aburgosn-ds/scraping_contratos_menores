#!/usr/bin/env python3
# scheduler.py - Run `main()` every hour with retries using APScheduler

from datetime import datetime, timedelta
import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from main_test import main as run_main
from utils.logger import setup_logger


logger = setup_logger()
scheduler = BlockingScheduler()

MAX_RETRIES = 3
RETRY_DELAY_MINUTES = 5
JOB_ID = 'hourly_scrape'


def run_and_handle(job_name=JOB_ID, attempt=1):
    logger.info("Job '%s' started (attempt %s)", job_name, attempt)
    try:
        run_main()
        logger.info("Job '%s' completed successfully", job_name)
    except Exception as e:
        logger.exception("Job '%s' failed on attempt %s: %s", job_name, attempt, e)
        if attempt < MAX_RETRIES:
            next_run = datetime.now() + timedelta(minutes=RETRY_DELAY_MINUTES)
            logger.info("Scheduling retry %s for job '%s' at %s", attempt + 1, job_name, next_run)
            # schedule a one-off retry job
            scheduler.add_job(
                run_and_handle,
                'date',
                run_date=next_run,
                args=[job_name, attempt + 1],
                id=f"{job_name}_retry_{attempt + 1}",
            )
        else:
            logger.error("Job '%s' reached max retries (%s). Will wait until next scheduled run.", job_name, MAX_RETRIES)


def start():
    logger.info("Scheduling hourly job starting now")
    # Schedule the main job to run every hour, starting immediately
    scheduler.add_job(run_and_handle, 'interval', hours=1, args=[JOB_ID, 1], next_run_time=datetime.now(), id=JOB_ID)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped by user")


if __name__ == "__main__":
    start()
