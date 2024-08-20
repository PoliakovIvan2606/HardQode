from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course
from users.models import Subscription, Balance


class PayForCourseView(APIView):
    """Покупка курса"""
    permission_classes = (IsAuthenticated,)

    def post(self, request, course_id, *args, **kwargs):
        if not course_id:
            return Response({'detail': 'Не указан идентификатор курса.'}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, id=course_id)
        user = request.user

        try:
            balance = Balance.objects.get(user=user)
        except Balance.DoesNotExist:
            return Response({'detail': 'Баланс не найден.'}, status=status.HTTP_404_NOT_FOUND)

        if balance.amount < course.price:
            return Response({'detail': 'Недостаточно бонусов.'}, status=status.HTTP_400_BAD_REQUEST)

        balance.amount -= course.price
        balance.save()

        Subscription.objects.create(user=user, course=course)
        
        return Response({'detail': 'Оплата прошла успешно. Доступ к курсу открыт.'}, status=status.HTTP_200_OK)


class AvailableCourseListView(generics.ListAPIView):
    """Список не купленных курсов"""
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        purchased_courses = Subscription.objects.filter(user=user).values_list('course_id', flat=True)
        return Course.objects.filter(is_available=True).exclude(id__in=purchased_courses)

class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""

        # TODO

        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )
