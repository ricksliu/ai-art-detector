from django.db import models


class SampleImage(models.Model):
    filename = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    src = models.CharField(max_length=255)
    src_id = models.IntegerField()
    src_url = models.URLField()
    src_timestamp = models.DateTimeField()
    src_is_ai_generated = models.BooleanField()

    class Meta:
        unique_together = ('src', 'src_id')

    def __str__(self):
        return self.filename
