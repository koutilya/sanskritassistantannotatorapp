from django.contrib import admin

# Register your models here.
from .models import Sentences,linetypes,WordOptions,Wordsinsentence

admin.site.register(Sentences)
admin.site.register(Wordsinsentence)
admin.site.register(WordOptions)
