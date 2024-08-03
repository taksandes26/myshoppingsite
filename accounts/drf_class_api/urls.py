from django.urls import path
from .views import SignupApiView, ProfileCreateApiView, ProfileUpdateApiView, ProfileDeleteApiView, ProfileDetailApiView

app_name = 'drf_class_api'

urlpatterns = [
    path('signup/', SignupApiView.as_view(), name='signup_api'),
    path('profiles/', ProfileDetailApiView.as_view(), name='profile_list_api'),
    path('profiles/<int:user_id>/', ProfileDetailApiView.as_view(), name='profile_detail_api'),
    path('create-profile/', ProfileCreateApiView.as_view(), name='create_profile_api'),
    path('update-profile/', ProfileUpdateApiView.as_view(), name='update_profile_api'),
    path('delete-profile/', ProfileDeleteApiView.as_view(), name='delete_profile_api'),
]
