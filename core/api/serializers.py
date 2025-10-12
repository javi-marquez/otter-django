from rest_framework import serializers

from .models import Following, Like, Retweet, TestModel, Tweet, User


class TestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = ["id", "name", "date"]


# --- User ---
class UserSerializer(serializers.ModelSerializer):
    tweets_count = serializers.IntegerField(read_only=True)
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "userName",
            "userNickname",
            "userBio",
            "userJoined",
            "tweets_count",
            "followers_count",
            "following_count",
        ]
        read_only_fields = [
            "id",
            "userJoined",
            "tweets_count",
            "followers_count",
            "following_count",
        ]


# --- Tweet (con campos computados + nested ids) ---
class TweetSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source="user", queryset=User.objects.all(), write_only=True
    )
    parentTweet_id = serializers.PrimaryKeyRelatedField(
        source="parentTweet",
        queryset=Tweet.objects.all(),
        write_only=True,
        allow_null=True,
        required=False,
    )

    likes_count = serializers.IntegerField(read_only=True)
    retweets_count = serializers.IntegerField(read_only=True)
    replies_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tweet
        fields = [
            "id",
            "tweetContent",
            "tweetDate",
            "tweetImage",
            "user_id",
            "parentTweet_id",
            "likes_count",
            "retweets_count",
            "replies_count",
        ]
        read_only_fields = [
            "id",
            "tweetDate",
            "likes_count",
            "retweets_count",
            "replies_count",
        ]


# --- Like ---
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "tweet", "likeDate"]
        read_only_fields = ["id", "likeDate"]
        # refuerza la unicidad (user, tweet)
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Like.objects.all(),
                fields=["user", "tweet"],
                message="Ya existe un like para este (user, tweet).",
            )
        ]


# --- Retweet ---
class RetweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retweet
        fields = ["id", "user", "tweet", "retweetDate"]
        read_only_fields = ["id", "retweetDate"]
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Retweet.objects.all(),
                fields=["user", "tweet"],
                message="Ya existe un retweet para este (user, tweet).",
            )
        ]


# --- Following ---
class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = ["id", "follower", "followed", "followingDate"]
        read_only_fields = ["id", "followingDate"]
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Following.objects.all(),
                fields=["follower", "followed"],
                message="Ya sigues a este usuario.",
            )
        ]
