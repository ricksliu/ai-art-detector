from django.db import models


class WebImage(models.Model):
    """
    Image request and model prediction.
    """

    filename = models.CharField(max_length=255)
    url = models.URLField(default='', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    model_version = models.CharField(max_length=255, default='', blank=True)
    model_prediction = models.DecimalField(max_digits=5, decimal_places=4, default=None, blank=True, null=True)

    def __str__(self):
        return self.filename
