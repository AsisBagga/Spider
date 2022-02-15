from django.db import models

# Create your models here.

class CrawlerModel(models.Model):
    base_url = models.CharField(max_length=500)
    site_links = models.TextField(default="No Site Map found")

    def __str__(self):
        return self.base_url