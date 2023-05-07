from django.db import models
from django.urls import reverse


class Category(models.Model):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Название категории'
    )

    slug = models.SlugField(
        max_length=256,
        unique=True,
        db_index=True,
        verbose_name='URL'
    )

    image = models.ImageField(
        blank=True,
        upload_to='img/category'
    )

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.PROTECT,
        verbose_name='Категория',
    )

    name = models.CharField(
        max_length=150,
        db_index=True,
        verbose_name=u'Название',
    )

    image = models.ImageField(
        upload_to='img/product',
        blank=True,
        verbose_name=u'Фото'
    )

    description = models.TextField(
        max_length=1000,
        blank=True,
        verbose_name=u'Описание'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=u'Цена',
    )

    available = models.BooleanField(
        default=True,
        verbose_name=u'Наличие',
    )

    slug = models.SlugField(
        max_length=150,
        db_index=True,
        unique=True,
        verbose_name=u'URL'
    )

    created = models.DateTimeField(auto_now_add=True)

    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
