from django.conf import settings

class MobileMiddleware(object):

    def process_request(self, request):
        domain = request.META.get('HTTP_HOST', '').split('.')
        
        if not ('m' in domain or 'mobile' in domain):
            settings.TEMPLATE_DIRS = settings.MOBILE_TEMPLATE_DIRS
        else:
            settings.TEMPLATE_DIRS = settings.DESKTOP_TEMPLATE_DIRS