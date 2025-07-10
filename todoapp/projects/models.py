
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from users.models import CustomUser as User


class Project(models.Model):
    """
        Needed fields
        - members (m2m field to CustomUser; create through table and enforce unique constraint for user and project)
        - name (max_length=100)
        - max_members (positive int)
        - status (choice field integer type :- 0(To be started)/1(In progress)/2(Completed), with default value been 0)

        Add string representation for this model with project name.
    """
    class StatusChoices(models.IntegerChoices):
        TO_BE_STARTED = 0, "To be started"
        IN_PROGRESS = 1, "In progress"
        COMPLETED = 2, "Completed"

    members = models.ManyToManyField(User, through='ProjectMember', related_name="project_working_on")
    name = models.CharField(max_length=100)
    max_members = models.PositiveSmallIntegerField()
    status = models.IntegerField(
        choices = StatusChoices.choices,
        default = StatusChoices.TO_BE_STARTED,
    )

    def __str__(self):
        return self.name

class ProjectMember(models.Model):
    """
    Needed fields
    - project (fk to Project model)
    - member (fk to User model - use AUTH_USER_MODEL from settings)
    - Add unique constraints

    Add string representation for this model with project name and user email/first name.
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('project','member')

    def __str__(self):
        return self.member.first_name

  

