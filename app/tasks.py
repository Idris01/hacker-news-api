from django_cron import CronJobBase, Schedule
from app.management.commands.updater import do_update


class NewsSyncronizer(CronJobBase):
    RUN_INTERVAL_MIN = 5
    FAILURE_RETRY_INTERVAL = 1
    schedule = Schedule(
        run_every_mins=RUN_INTERVAL_MIN, retry_after_failure_mins=FAILURE_RETRY_INTERVAL
    )
    code = "app.news_update_cron_job"

    def do(self):
        try:
            do_update()
        except Exception as e:
            self.stdout.write(self.style.SUCCESS(f"Error: {e}"))
        self.stdout.write(self.style.SUCCESS("database updated"))
