from django.db import models
from django.conf import settings


class Spends(models.Model):
    payer = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.PROTECT)
    category = models.ForeignKey("Categories", null=True,
                                 on_delete=models.SET_NULL)
    cost = models.FloatField()
    comment = models.CharField("Comment", max_length=200)
    cost_date = models.DateField()
    input_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return '/account/'

    def __str__(self):
        return f'{self.payer}, {self.category}, {self.cost}, {self.comment}'

    class Meta:
        ordering = ['-cost_date']


class Payers(models.Model):
    name = models.CharField("Name", max_length=50)

    def __str__(self):
        return self.name


class Categories(models.Model):
    category_name = models.CharField("Category", max_length=50)

    def get_absolute_url(self):
        return '/account/'

    def __str__(self):
        return self.category_name


class Subcategory(models.Model):
    category = models.ForeignKey("Categories", on_delete=models.CASCADE)
    subcategory_name = models.CharField("Subcategory", max_length=50)

    def __str__(self):
        return self.subcategory_name
