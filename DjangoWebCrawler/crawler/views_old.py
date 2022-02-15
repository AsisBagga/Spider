from django.shortcuts import render

# Create your views here.

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from crawler.models import CrawlerModel
from crawler.serializers import CrawlerSerialzer

from bs4 import BeautifulSoup
import requests, json


class SiteLists(APIView):
    """
    List all SiteMaps, or create a new SiteMap.
    """

    def get(self, request, format=None):
        """
            Gets all the links saved.
        """
        siteMap = CrawlerModel.objects.all()
        serializer = CrawlerSerialzer(siteMap, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        """
            This method takes in the base url for crawling and returns a dictionary with all the links till depth of level 1
        """
        new_data = {"base_url": request.data["base_url"]}
        check = CrawlerModel.objects.filter( base_url= new_data["base_url"])
        # returns querySet if it already exists...
        if check.exists():
            return Response(check.values()[0]["site_links"])
        # extracts the site links
        new_data["site_links"] = str(self._only_Level_1(request.data["base_url"]))
        serializer = CrawlerSerialzer(data=new_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data["site_links"], status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _extract_urls(self, base_url):
        """
            This internal method primarely scrapes the links and filter to its domain.
        """
        final = dict()
        my_domain = base_url.replace("https://", "")
        try:
            response = requests.get(base_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            final[base_url] = []
            for link in soup.find_all('a', href=True):
                if my_domain in link['href']:
                    final[base_url].append({link['href']: list()})
            return final
        except:
            return    
        
    def _only_Level_1(self, my_url):
        """
            This internal methods extract all the urls till level 1 (considering level 0 as base level) .
        """
        x = self._extract_urls(my_url)
        for i in range(0, len(x[my_url])):
            x[my_url][i] = self._extract_urls(list(x[my_url][i].keys())[0])    
        return x           
