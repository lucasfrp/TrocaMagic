from django.contrib import admin
import models

class CardAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(models.Layout)
admin.site.register(models.Color)
admin.site.register(models.Supertype)
admin.site.register(models.Type)
admin.site.register(models.Rarity)
admin.site.register(models.Artist)
admin.site.register(models.Subtype)
admin.site.register(models.Card, CardAdmin)
admin.site.register(models.NamesCard)
admin.site.register(models.Set)
admin.site.register(models.TypeSet)

