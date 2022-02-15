from random import betavariate
import re
import requests
from bs4 import BeautifulSoup
import json 
from timeit import default_timer as timer
from datetime import timedelta

my_url = "https://food.com"
my_domain = my_url.replace("https://", "")

The_great_list = []
queue =[]
# def get(my_url):
#     """ 
#     This method takes a url and adds list of new urls to the The_great_list
#     """
#     try:   
#         response = requests.get(my_url)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         for link in soup.find_all('a', href=True):
#             # Here I need to consider links that only starts with /Testimonials or /page
#             if my_domain in link['href'] and link['href'] not in The_great_list:
#                 The_great_list.append(link['href'])
#                 if link['href'] not in queue:
#                     queue.append(link['href'])
#     except:
#         return

def extract_urls(base_url):
    try:
        start = timer()
        response = requests.get(base_url)
        end=timer()
        print("REQUEST TAKES: ", timedelta(seconds=end-start))
        soup = BeautifulSoup(response.text, 'html.parser')
        final = []
        for link in soup.find_all('a', href=True):
            if my_domain in link['href']:
                final.append(link['href'])
        
        return final
    except:
        return    
        
class TreeNode:
    tree = ""
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None        
    
    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level
    
    def add_child(self,child):
        #level = self.get_level()
        #if level < 2:
        child.parent = self
        self.children.append(child)

    def print_tree(self):
        spaces = " " * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        TreeNode.tree = TreeNode.tree + prefix + self.data + "\n"
        if self.children:
            for child in self.children:
                child.print_tree()
        return TreeNode.tree

def build(root, count):
    count += 1
    if count > 1:
        return None
    print("$$ VALUE OF ROOT: ",root.data)
    # if root.get_level() > 0:
    #     print("## RETURNING NONE")
    #     return None
    listOfUrls = extract_urls(root.data)
    for i in listOfUrls:
        #print("@@ VALUE I: ", i)
        iTree = TreeNode(data=i)
        root.add_child(iTree)
        build(iTree, count)
#        listOfUrlsTwo = extract_urls(iTree.data)
#        for j in listOfUrlsTwo:
#            jTree = TreeNode(data=j)
#            iTree.add_child(jTree)    
start = timer()

count = 0
root = TreeNode(data=my_url)
build(root, count)
print(root.print_tree())

end = timer()
print("PERFORMANCE: ", timedelta(seconds=end-start))


# for i in range(0, len(x[my_url])):
#     x[my_url][i] = extract_urls(list(x[my_url][i].keys())[0])
# print(len(x))

# 
#     f.write(str(json.dumps(x, sort_keys=False, indent=4)))

#print(json.dumps(x, sort_keys=False, indent=4))                