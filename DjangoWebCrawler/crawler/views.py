from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from crawler.models import CrawlerModel
from crawler.serializers import CrawlerSerialzer

from bs4 import BeautifulSoup
import requests

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class SiteLists(APIView):
    def post(self, request, format=None):
        """
            it takes in the base url for crawling 
            and returns a dictionary with all the links till depth of level 2
        """
        # checking if base_url exist in client request.
        if "base_url" not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        new_data = {"base_url": request.data["base_url"]}
        depth = int(request.data["depth"])
        # try chache hit
        if cache.get(new_data["base_url"]):
            print("$$$$$CACHE HIT")
            return Response(cache.get(new_data["base_url"]))

        # in case of cache miss
        root = TreeNode(data=request.data["base_url"])
        SiteLists._build(root=root, depth=depth)
        new_data["site_links"] = root.print_tree()
        cache.set(new_data["base_url"], new_data["site_links"])
        print("&&&CACHE SET!")

        serializer = CrawlerSerialzer(data=new_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data["site_links"], status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _build(root, depth, count=0):
        """
        This is a utility method which is used to build tree of urls.
        Args:
            count: Depth of the tree 
            root: TreeNode
        """
        count += 1
        if count > depth:
            return None
        listOfUrls = SiteLists._extract_urls(root.data)
        if listOfUrls:
            for i in listOfUrls:
                iTree = TreeNode(data=i)
                root.add_child(iTree)
                SiteLists._build(root=iTree, count=count, depth=depth)

    def _extract_urls(base_url):
        """
        This is a utility method which scarpes the webpage to fetch the links.
        Args: 
            base_url: url to be crawled
        Returns:
            list of urls with the similar domain.
        """
        my_domain = base_url.replace("https://", "")
        try:
            response = requests.get(base_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            final = []
            for link in soup.find_all('a', href=True):
                if my_domain in link['href'] and link['href'] not in final:
                    final.append(link['href'])
            return final
        except:
            return  

class TreeNode:
    """
    using TreeNode to store the urls and linking each one with a parent and childrens
    """
    tree = ""
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None
    
    def get_level(self):
        """
        Returns:
            depth of the node.
        """
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level
    
    def add_child(self,child):
        """
        adds child node to a parent node
        Args:
            child: TreeNode to be add to a parent
        """
        child.parent = self
        self.children.append(child)

    def print_tree(self):
        """
        this method is used to form the tree/site map
        updates the class variable through recursion and returns it
        """
        spaces = " " * self.get_level() * 4 # Tab
        prefix = spaces + "|__" if self.parent else ""
        TreeNode.tree = TreeNode.tree + prefix + self.data + "\n"
        if self.children:
            for child in self.children:
                child.print_tree()
        return TreeNode.tree