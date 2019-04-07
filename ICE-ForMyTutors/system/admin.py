from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(ComponentText)
admin.site.register(ComponentImage)
admin.site.register(Enroll)
admin.site.register(Category)
