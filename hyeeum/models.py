from django.db import models

# Create your models here.
# 역참조시 related_name쓰기만 하면 됨.
# 혹시 모르니 related_name, serializer 변수이름, serializer 출력시 이름을 맞추도록 하자
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    user_tag = models.IntegerField(unique=True) # 이거랑 id랑 구분짓는거 너무 비효율적
    created_at = models.DateTimeField(auto_now_add=True)
    birth = models.DateField()
    alignment = models.CharField(max_length=100)
    template = models.BooleanField(default=False)
    polite = models.BooleanField(default=False)
    library_count = models.IntegerField(default=0)

class Library(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='librarys')
    book_count = models.IntegerField(default=0)

def upload_to_image(instance, filename):
    return f'{instance.library_id.user_id.id}/{instance.library_id.id}/{filename}'

class Book(models.Model):
    EMOTIONS = [
        ('기쁨', '기쁨'),
        ('화남', '화남'),
        ('슬픔', '슬픔'),
        ('즐거움', '즐거움'),
    ]
    id = models.AutoField(primary_key=True)
    library_id = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='books')
    image = models.ImageField(upload_to=upload_to_image)
    comment = models.TextField(blank=True)
    detail_story = models.TextField(blank=True)
    emotion = models.CharField(max_length=10, choices=EMOTIONS)
    created_at = models.DateTimeField(auto_now_add=True)

class Statistics(models.Model):
    id = models.AutoField(primary_key=True)
    library_id = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='statistics')
    happiness = models.IntegerField(default=0)
    aggro = models.IntegerField(default=0)
    sadness = models.IntegerField(default=0)
    joy = models.IntegerField(default=0)
    gpt_comment = models.CharField(max_length=500, default="")