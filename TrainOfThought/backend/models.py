from django.db import models

class Creator(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='creators/', null=True, blank=True)
    description = models.CharField(max_length=150)
    default_reputation = models.FloatField()
    default_hatred = models.FloatField()
    default_popularity = models.FloatField()
    networth = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Bot(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    reputation = models.FloatField()
    hatred = models.FloatField()
    likeness = models.FloatField()
    popularity = models.FloatField()
    networth = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    likes = models.PositiveIntegerField(default=0)
    reposts = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Post {self.id} by {self.bot.name}"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    reposts = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Comment on Post {self.post.id}"