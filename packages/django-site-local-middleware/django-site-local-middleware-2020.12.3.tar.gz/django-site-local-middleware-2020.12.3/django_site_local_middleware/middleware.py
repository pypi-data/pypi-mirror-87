#!/usr/bin/env python
from django.conf import settings
from django.contrib.sites.models import Site

class SiteLocalMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response = self.process_response(request, response)
        return response

    def process_response(self,request, response):
        if settings.DEBUG and hasattr(response,'content'):
            port = request.get_port()
            content = response.content.decode()
            for site in Site.objects.all():
                domain = site.domain
                content = content.replace('%s:' % domain, '%s.local:' % domain).replace('%s/' % domain, '%s.local:%s/' % (domain,request.get_port()))
            response.content = content.encode()
        return response
