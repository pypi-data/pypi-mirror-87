#!/usr/bin/env python
from django.conf import settings
from django.contrib.sites.models import Site


HOST_SITE_IDS = {}
for site in Site.objects.all():
    HOST_SITE_IDS[site.domain] = site.id

class SiteIdMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        return response

    def process_request(self, request):
        global HOST_SITE_IDS
        host = request.get_host()
        if host in HOST_SITE_IDS:
            settings.SITE_ID =  HOST_SITE_IDS[host]
            return
        for _host in [host.split(':')[0],host.split(':')[0].replace('.local','')]:
            if _host in HOST_SITE_IDS:
                HOST_SITE_IDS[host] = HOST_SITE_IDS[_host]
                settings.SITE_ID = HOST_SITE_IDS[host]
