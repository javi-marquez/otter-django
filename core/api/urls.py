from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import (
    FollowingViewSet,
    LikeViewSet,
    RetweetViewSet,
    TweetViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"tweets", TweetViewSet, basename="tweet")
router.register(r"likes", LikeViewSet, basename="like")
router.register(r"retweets", RetweetViewSet, basename="retweet")
router.register(r"following", FollowingViewSet, basename="following")

urlpatterns = [
    path("api/", include(router.urls)),
    path("test/", views.TestModelCreate.as_view(), name="test-view-create"),
]
