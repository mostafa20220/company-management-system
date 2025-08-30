import logging

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User
from .models import PerformanceReview
from .serializers import (
    PerformanceReviewSerializer, ReviewScheduleSerializer,
    ReviewFeedbackSerializer, ReviewRejectSerializer
)
from users.permissions import IsManager, IsAdmin, IsOwnerOrManagerOrAdmin

logger = logging.getLogger(__name__)

class PerformanceReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing the Employee Performance Review Cycle.
    """
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrManagerOrAdmin]

    def get_queryset(self):
        """
        Filter reviews based on user role.
        - Admins see all.
        - Managers see reviews for their department's employees.
        - Employees see their own review.
        """
        user = self.request.user
        if user.role == User.Role.ADMIN:
            return PerformanceReview.objects.all()
        elif user.role == User.Role.MANAGER:
            try:
                return PerformanceReview.objects.filter(employee__department=user.employee.department)
            except:
                return PerformanceReview.objects.none()
        elif user.role == User.Role.EMPLOYEE:
            try:
                return PerformanceReview.objects.filter(employee=user.employee)
            except:
                return PerformanceReview.objects.none()
        return PerformanceReview.objects.none()

    # --- Custom Actions for FSM Transitions ---

    @action(detail=True, methods=['post'], permission_classes=[IsManager | IsAdmin])
    def schedule(self, request, pk=None):
        """Transition: Pending Review -> Review Scheduled"""
        review = self.get_object()
        serializer = ReviewScheduleSerializer(data=request.data)
        if serializer.is_valid():
            try:
                review.review_date = serializer.validated_data['review_date']
                review.schedule_review()
                review.save()
                logger.info(f'Review {review.id} scheduled for employee {review.employee.id} by user {request.user.id}.')
                return Response({'status': 'Review scheduled'}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f'Failed to schedule review {review.id} by user {request.user.id}. Error: {e}',)
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsManager | IsAdmin])
    def provide_feedback(self, request, pk=None):
        """Transition: Review Scheduled -> Feedback Provided"""
        review = self.get_object()
        serializer = ReviewFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            try:
                review.provide_feedback(feedback_text=serializer.validated_data['feedback_text'])
                review.save()
                logger.info(f'Feedback provided for review {review.id}'
                            f' for employee {review.employee.id} by user {request.user.id}.')
                return Response({'status': 'Feedback provided'}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f'Failed to provide feedback for review {review.id} by user {request.user.id}. Error: {e}',)
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsManager | IsAdmin])
    def submit_for_approval(self, request, pk=None):
        """Transition: Feedback Provided -> Under Approval"""
        review = self.get_object()
        try:
            review.submit_for_approval()
            review.save()
            logger.info(f'Submitted review for {review.id}'
                        f' for employee {review.employee.id} by user {request.user.id}.')
            return Response({'status': 'Submitted for approval'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Failed to submit review {review.id} for approval by user {request.user.id}. Error: {e}',)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsManager | IsAdmin])
    def approve(self, request, pk=None):
        """Transition: Under Approval -> Review Approved"""
        review = self.get_object()
        try:
            review.approve_review()
            review.save()
            logger.info(
                f"Performance review {review.id} for employee {review.employee.id} "
                f"was APPROVED by user {request.user.id}."
            )
            logger.error(
                f"Failed to approve review {review.id} for user {request.user.id}. Error: {e}",
                exc_info=True # Adds stack trace to the log
            )
            return Response({'status': 'Review approved'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsManager | IsAdmin])
    def reject(self, request, pk=None):
        """Transition: Under Approval -> Review Rejected"""
        review = self.get_object()
        serializer = ReviewRejectSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Add the rejection reason to the existing feedback for context.
                rejection_note = f"\n\n--- REJECTED ---\n{serializer.validated_data['rejection_feedback']}"
                review.reject_review(rejection_note=rejection_note)
                review.save()
                logger.warning(
                    f"Performance review {review.id} for employee {review.employee.id} "
                    f"was REJECTED by user {request.user.id}."
                )
                return Response({'status': 'Review rejected, feedback required'}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(
                    f"Failed to reject review {review.id} for user {request.user.id}. Error: {e}",
                    exc_info=True
                )
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
