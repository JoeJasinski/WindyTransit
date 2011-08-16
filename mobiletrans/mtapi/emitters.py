from piston.emitters import XMLEmitter, Emitter
from django.utils.encoding import smart_unicode
from piston.utils import HttpStatusCode, Mimer



class xmlTransitRouteEmitter(XMLEmitter):
    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):
            for item in data:
                xml.startElement("stop", {})
                self._to_xml(xml, item)
                xml.endElement("stop")
        elif isinstance(data, dict):
            for key, value in data.iteritems():
                xml.startElement(key, {})
                self._to_xml(xml, value)
                xml.endElement(key)
        else:
            xml.characters(smart_unicode(data))


Emitter.register('routexml', xmlTransitRouteEmitter, 'text/xml; charset=utf-8')
Mimer.register(lambda *a: None, ('application/xml',))



class xmlTransitRoutesEmitter(XMLEmitter):
    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):
            for item in data:
                xml.startElement("transit_route", {})
                self._to_xml(xml, item)
                xml.endElement("transit_route")
        elif isinstance(data, dict):
            for key, value in data.iteritems():
                xml.startElement(key, {})
                self._to_xml(xml, value)
                xml.endElement(key)
        else:
            xml.characters(smart_unicode(data))


Emitter.register('routesxml', xmlTransitRoutesEmitter, 'text/xml; charset=utf-8')
Mimer.register(lambda *a: None, ('application/xml',))



class xmlLocationEmitter(XMLEmitter):
    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):
            for item in data:
                xml.startElement("location", {})
                self._to_xml(xml, item)
                xml.endElement("location")
        elif isinstance(data, dict):
            for key, value in data.iteritems():
                xml.startElement(key, {})
                self._to_xml(xml, value)
                xml.endElement(key)
        else:
            xml.characters(smart_unicode(data))


Emitter.register('locxml', xmlLocationEmitter, 'text/xml; charset=utf-8')
Mimer.register(lambda *a: None, ('application/xml',))



class newlineTransitStopEmitter(Emitter):
    def render(self, request, format='xml'):
        response = self.data
        try:
            response = '\n'.join(map(lambda x: x['uuid'], response.items()[0][1]))
        except:
            response = ''
        return response

Emitter.register('newline', newlineTransitStopEmitter, 'text/plain; charset=utf-8')