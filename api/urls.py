from django.urls import path, include

from .viewsets import *

urlpatterns = [
    path('create/', SponsorCreate.as_view()),
    path('list/', SponsorList.as_view()),
    path('<int:pk>/', Sponsor.as_view()),
    path('update/<int:pk>', SponsorUpdate.as_view()),
    # path('get_sponsor/', get_sponsor),
    path('donations/', DonationsView.as_view()),
    path('donations/<int:pk>/', DonationDetailView.as_view()),
]
