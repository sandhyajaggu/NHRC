from app.models.job import Job


class JobService:

    @staticmethod
    def get_my_jobs(
        db,
        membership_id
    ):

        jobs = db.query(Job).filter(
            Job.created_by == membership_id
        ).all()

        return jobs