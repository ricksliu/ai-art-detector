from django.db import models


class RequestImage(models.Model):
    filename = models.CharField(max_length=255)
    url = models.URLField(default='', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_ai_generated = models.BooleanField(default=None, blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = ''

    def __str__(self):
        return self.filename
