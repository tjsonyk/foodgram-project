from django.db import models
from django.contrib.auth import get_user_model

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
    METRIC = 'M'
    SPECULATIVE = 'S'
    ENGLISH = 'U'
    TYPES_OF_UNIT = (
        (METRIC, 'Метрическая'),
        (SPECULATIVE, 'Умозрительная'),
        (ENGLISH, 'Английская')
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
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Amount',
        through_fields=('recipe', 'ingredient'),
        )
    tags = models.ManyToManyField(Tag)
    cooking_time = models.PositiveSmallIntegerField(default=1)
    slug = models.SlugField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)

    def get_ingredients(self):
        return Recipe.objects.value_list('ingredients')

    def __str__(self):
        return str(self.title)

    def __unicode__(self):
        return "{0}".format(self.title)


class Amount(models.Model):
    amount = models.PositiveSmallIntegerField(default=1)
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amount'
        )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.ingredient.dimension)


class Favors(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favor_by')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favor')

    def __str__(self):
        return self.recipe.title


class ShopList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='buyer')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.recipe.title


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following')

    def __str__(self):
        return self.user.username
