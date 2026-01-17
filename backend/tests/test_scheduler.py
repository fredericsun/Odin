from app.scheduler import build_scheduler


def test_build_scheduler_has_jobs():
    scheduler = build_scheduler(lambda: None, lambda: None, report_hour_local=7)
    job_ids = {job.id for job in scheduler.get_jobs()}
    assert "run-once" in job_ids
    assert "daily-report" in job_ids
