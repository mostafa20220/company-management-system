from rest_framework import serializers
from .models import PerformanceReview

class PerformanceReviewSerializer(serializers.ModelSerializer):
    """
    Main serializer for the PerformanceReview model.
    """
    employee_name = serializers.CharField(source='employee.user.get_full_name', read_only=True)
    # Provides the human-readable name of the current state (e.g., "Pending Review").
    state_display = serializers.CharField(source='get_state_display', read_only=True)

    class Meta:
        model = PerformanceReview
        fields = ('id', 'employee', 'employee_name', 'state', 'state_display', 'feedback', 'review_date')
        # The state is read-only because it should only be changed via the defined FSM transitions.
        read_only_fields = ('state',)

# --- Action-Specific Serializers ---
# These small serializers are used to validate the input for custom viewset actions.

class ReviewScheduleSerializer(serializers.Serializer):
    """Serializer for scheduling a review."""
    review_date = serializers.DateTimeField(required=True)

class ReviewFeedbackSerializer(serializers.Serializer):
    """Serializer for providing feedback."""
    feedback_text = serializers.CharField(required=True, style={'base_template': 'textarea.html'})

class ReviewRejectSerializer(serializers.Serializer):
    """Serializer for rejecting a review."""
    feedback_text = serializers.CharField(required=True, style={'base_template': 'textarea.html'})
