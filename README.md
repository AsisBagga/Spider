# Spider Crawler
A simple web crawler service named spider (server and client) built in Django/Python language. Client script is available in Golang and Python language. The server would receive requests from a client to crawl a URL and should send the response i.e sitemap back to the client. 
Client will do a POST request with data as json would look like:
``` 
{
    "base_url": "https://foobar.com/baz",
    "depth": 2,
} 
```

- `base_url` - The URL to be crawled.
- `depth` - The depth to which you expect the spider to crawl.

The Service/Server which is crawler is limited to one domain - so when you start with `https://redhat.com/foo/bar`, it would crawl all pages within redhat.com, but not follow external links, for example to Facebook and Twitter accounts. 
So, given a URL, the client send requests for the url to be crawled and should print a simple sitemap, showing the links between pages. E.g. given http://foobar.com/baz the client may print the sitemap in a tree form as follows 
```
foobar.com/baz 
    - bar/ 
        - xyz 
        - abc 
        - mno 
    - about 
    - contacts 
        - has 
            - more links 
            - more links 
            - more links 
```
## Server deployment:
Server is deployed in a Kuberenets cluster. The docker image of server is available in docker hub at [asis80/spider](https://hub.docker.com/repository/registry-1.docker.io/asis80/spider/) with tag `redis`

### Details Steps to run the project in your local system:
Prerequists: 
    Docker, kubectl and minikube should be already installed in your local system. 

- Step 1: clone the project to your local system.
    - ` git clone https://github.com/AsisBagga/Django-WebCrawler.git`
- Step 1: Run k8s deployment manifest
    - ` kubectl apply -f deployment-definition.yaml `
- Step 2: Run your K8s service manifest
    - ` kubectl apply -f service-definitation.yaml `
- Step 3: Do port forwarding
    - minikube: 
        - minikube service django-spider —url
    - K8s Cluster without LoadBalancer:
        - kubectl port-forward deploy/django-spider 8080:8000
- Step 5: Once your deployment pods are running goto chorme to verify its reachable at 127.0.0.1:8080/crawler/
- Step 6: If it is reachable over chrome then run your client.py file as `python client.py` it would revert with a sitemap. 

> Note: if you may find any issues, I am reachable at asisbagga@gmail.com. Although, you can login to the pod to check if redis-server is up by running command `redis-cli ping` it should reply as "PONG" 
