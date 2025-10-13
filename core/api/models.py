from django.db import models


# Create your models here.
class TestModel(models.Model):
    """Clase para testing"""

    name = models.TextField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class User(models.Model):
    userName = models.CharField(max_length=50, unique=True)
    userNickname = models.CharField(max_length=50)
    userBio = models.CharField(max_length=255, blank=True, null=True)
    userJoined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.userName)


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets")
    parentTweet = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="replies",
    )
    tweetContent = models.CharField(max_length=255)
    tweetDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.userName}: {self.tweetContent[:30]}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="likes")
    likeDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "tweet")

    def __str__(self):
        return f"{self.user.userName} ❤️ {self.tweet_id}"


class Retweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="retweets")
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="retweets")
    retweetDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "tweet")

    def __str__(self):
        return f"RT {self.user.userName} → {self.tweet_id}"


class Following(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )
    followingDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "followed")

    def __str__(self):
        return f"{self.follower.userName} ➜ {self.followed.userName}"
