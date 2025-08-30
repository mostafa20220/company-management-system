from django.db import models
from django_fsm import FSMField, transition
from organizations.models import Employee
from companyManagementSystem.models import TimeBaseModel
from django.utils.translation import gettext_lazy as _

class PerformanceReview(TimeBaseModel, models.Model):
    class Stages(models.TextChoices):
        PENDING = 'PENDING', _('Pending Review')
        SCHEDULED = 'SCHEDULED', _('Review Scheduled')
        FEEDBACK = 'FEEDBACK', _('Feedback Provided')
        APPROVAL = 'APPROVAL', _('Under Approval')
        APPROVED = 'APPROVED', _('Review Approved')
        REJECTED = 'REJECTED', _('Review Rejected')

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performance_reviews')
    state = FSMField(default=Stages.PENDING, choices=Stages.choices, protected=True)
    feedback = models.TextField(blank=True)
    review_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Review for {self.employee} - {self.get_state_display()}"

    # --- State Transitions ---

    @transition(field=state, source=Stages.PENDING, target=Stages.SCHEDULED)
    def schedule_review(self, review_date):
        self.review_date = review_date

    @transition(field=state, source=Stages.SCHEDULED, target=Stages.FEEDBACK)
    def provide_feedback(self, feedback_text):
        self.feedback = feedback_text

    @transition(field=state, source=Stages.FEEDBACK, target=Stages.APPROVAL)
    def submit_for_approval(self):
        pass

    @transition(field=state, source=Stages.APPROVAL, target=Stages.APPROVED)
    def approve(self):
        pass

    @transition(field=state, source=Stages.APPROVAL, target=Stages.REJECTED)
    def reject(self, rejection_feedback):
        self.feedback += f"\n\n--- REJECTION ---\n{rejection_feedback}"

    @transition(field=state, source=Stages.REJECTED, target=Stages.FEEDBACK)
    def rework_feedback(self, updated_feedback):
        self.feedback = updated_feedback
