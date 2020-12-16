from django.contrib import admin

from .models import Spends, Categories, Payers, Subcategory


class SubcategoryInLine(admin.TabularInline):
    model = Subcategory
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubcategoryInLine]


class SpendAdmin(admin.ModelAdmin):
    list_display = ('category', 'cost', 'payer', 'comment', 'cost_date')


# Register your models here.
admin.site.register(Spends, SpendAdmin)
admin.site.register(Categories, CategoryAdmin)
admin.site.register(Subcategory)
admin.site.register(Payers)
