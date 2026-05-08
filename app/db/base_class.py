from app.db.base import Base

# import all models here

from app.models.member import Member

from app.models.employee import Employee

from app.models.student import (
    StudentUniversityDetails,
    StudentAutonomousDetails
)

from app.models.representative import (
    RepresentativeUniversityDetails,
    RepresentativeAutonomousDetails,
    RepresentativeBothDetails
)

from app.models.job import Job

from app.models.job_application import JobApplication