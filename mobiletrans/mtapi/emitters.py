from piston.emitters import XMLEmitter, Emitter
from django.utils.encoding import smart_unicode
from piston.utils import HttpStatusCode, Mimer



class xmlTransitRouteEmitter(XMLEmitter):
    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):
            for item in data:
                xml.startElement("transit_list", {})
                self._to_xml(xml, item)
                xml.endElement("transit_list")
        elif isinstance(data, dict):
            for key, value in data.iteritems():
                xml.startElement(key, {})
                self._to_xml(xml, value)
                xml.endElement(key)
        else:
            xml.characters(smart_unicode(data))


Emitter.register('routexml', xmlTransitRouteEmitter, 'text/xml; charset=utf-8')
Mimer.register(lambda *a: None, ('application/xml',))
