from django.contrib import admin
from .models import *

admin.site.register(Cinema)
admin.site.register(MovieRating)
admin.site.register(PasswordResetToken)