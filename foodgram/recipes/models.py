from django.db import models
# from users.models import CustomUser
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()


class Tag(models.Model):
    value = models.CharField(
        'Значение',
        max_length=255)
    style = models.CharField(
        'Постфикс для стиля шаблона',
        max_length=255,
        null=True)
    name = models.CharField(
        'Имя тега в шаблоне',
        max_length=255,
        null=True)

    def __str__(self):
       return self.name


class Dimension(models.Model):
    TYPES_OF_UNIT = (
        ('M', 'Метрическая'),
        ('S', 'Умозрительная'),
        ('U', 'Английская')
    )
    title = models.CharField(
        max_length=30,
        verbose_name='Единица измерения'
    )
    type_of_unit = models.CharField(max_length=1, choices=TYPES_OF_UNIT)
    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название ингридиента'
        )
    dimension = models.ForeignKey(Dimension, on_delete=models.RESTRICT)
    amount = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
        )
    title = models.CharField(
        max_length=100,
        verbose_name='Название рецепта'
        )
    image = models.ImageField(upload_to='recipes/', null=True)
    text = models.TextField()
    ingredient = models.ManyToManyField(Ingredient)
    tag = models.ManyToManyField(Tag)
    cooking_time = models.DurationField(default=timedelta(minutes=1))
    slug = models.SlugField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    
    def __str__(self):
        return self.title

        class Meta:
            ordering = ('-pub_date',)
