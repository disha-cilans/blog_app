from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from blogs import views

# Create a router and register our viewsets with it.
# router = DefaultRouter()
# router.register(r'blogs', views.BlogList)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('blogs/', views.BlogList.as_view()),
    path('blogs/<int:pk>/',views.BlogDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)