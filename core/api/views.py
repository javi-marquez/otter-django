from django.db.models import Count
from django.db.models.functions import Coalesce
from rest_framework import generics, mixins, viewsets

from .models import Following, Like, Retweet, TestModel, Tweet, User
from .serializers import (
    FollowingSerializer,
    LikeSerializer,
    RetweetSerializer,
    TestModelSerializer,
    TweetSerializer,
    UserSerializer,
)


class TestModelCreate(generics.ListCreateAPIView):
    queryset = TestModel.objects.all()
    serializer_class = TestModelSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.annotate(
        tweets_count=Coalesce(Count("tweets", distinct=True), 0),
        followers_count=Coalesce(Count("followers", distinct=True), 0),
        following_count=Coalesce(Count("following", distinct=True), 0),
    ).all()
    serializer_class = UserSerializer


class TweetViewSet(viewsets.ModelViewSet):
    queryset = (
        Tweet.objects.select_related("user", "parentTweet")
        .annotate(
            likes_count=Coalesce(Count("likes", distinct=True), 0),
            retweets_count=Coalesce(Count("retweets", distinct=True), 0),
            replies_count=Coalesce(Count("replies", distinct=True), 0),
        )
        .all()
    )
    serializer_class = TweetSerializer


class LikeViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Like.objects.select_related("user", "tweet").all()
    serializer_class = LikeSerializer


class RetweetViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Retweet.objects.select_related("user", "tweet").all()
    serializer_class = RetweetSerializer


class FollowingViewSet(viewsets.ModelViewSet):
    queryset = Following.objects.select_related("follower", "followed").all()
    serializer_class = FollowingSerializer
