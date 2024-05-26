from django.contrib import admin

# Register your models here.
from .models import ModelVersion,AIModel,Query,ExplainingAlgo,Explanation,Feedback
admin.site.register(AIModel)
admin.site.register(ModelVersion)
admin.site.register(Query)
admin.site.register(Feedback)
admin.site.register(ExplainingAlgo)
admin.site.register(Explanation)
