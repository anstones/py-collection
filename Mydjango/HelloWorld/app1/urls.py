from django.conf.urls import url
from app1 import views

urlpatterns = [
    # url(r'^login/', views.LoginView.as_view()),
    # url(r'^courses/', views.CourseView.as_view()),
    url(r'^publishes/', views.PublishView.as_view()),

]