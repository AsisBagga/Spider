from rest_framework import serializers
from crawler.models import CrawlerModel

class CrawlerSerialzer(serializers.ModelSerializer):
    class Meta:
        model = CrawlerModel
        fields = ['base_url', 'site_links']