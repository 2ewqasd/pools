from django.contrib import admin
from .models import Pool
from .models import Question
from .models import SuggestedAnswer
from .models import Answer

admin.site.register(Pool)
admin.site.register(Question)
admin.site.register(SuggestedAnswer)
admin.site.register(Answer)