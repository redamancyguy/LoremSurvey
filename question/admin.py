from django.contrib import admin

# Register your models here.
import user.models as u_models
admin.site.register(u_models.User)