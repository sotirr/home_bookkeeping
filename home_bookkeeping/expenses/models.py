from django.db import models
from django.conf import settings
from django.urls import reverse


class Spends(models.Model):
    '''
    Stores a list of spends. Related with Categories.
    '''
    payer = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.PROTECT)
    category = models.ForeignKey("Categories", null=True,
                                 on_delete=models.SET_NULL)
    cost = models.FloatField()
    comment = models.CharField("Comment", max_length=200)
    cost_date = models.DateField()
    input_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('expenses:index')

    def __str__(self):
        return f'{self.payer}, {self.category}, {self.cost}, {self.comment}'

    class Meta:
        ordering = ['-cost_date']


class Categories(models.Model):
    '''
    Stores categories
    '''
    category_name = models.CharField("Category", max_length=50)

    def get_absolute_url(self):
        return reverse('expenses:index')

    def __str__(self):
        return self.category_name
