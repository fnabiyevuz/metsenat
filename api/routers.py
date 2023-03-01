from rest_framework import routers

from .viewsets import StudentsViewSet

router = routers.DefaultRouter()
router.register('students', StudentsViewSet)
