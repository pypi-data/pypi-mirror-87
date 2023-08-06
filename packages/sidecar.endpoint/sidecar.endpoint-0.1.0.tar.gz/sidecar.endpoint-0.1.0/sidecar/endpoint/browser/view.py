from Products.Five.browser import BrowserView
from plone import api

import logging
logger = logging.getLogger(__name__)

class EndpointView(BrowserView):

    def __call__(self):

	request = self.request
        request.response.setHeader('Content-Type', 'text/plain')

	if request['method'] == 'POST':

		form = request.form
		endpoints = form.get('endpoints','')

                logger.info('Endpoints recebidos: ' + str(endpoints))

                if endpoints:
    		    endpoints = eval(endpoints)

                    logger.info('Registrando endpoints: ' + str(tuple(endpoints)))
    		    api.portal.set_registry_record('plone.cachepurging.interfaces.ICachePurgingSettings.cachingProxies', tuple(endpoints))
        	    logger.info('Endpoints gravados com sucesso.')

	output = api.portal.get_registry_record('plone.cachepurging.interfaces.ICachePurgingSettings.cachingProxies')

        if not output:
            output = tuple()
        
        logger.info('Retornando: ' + str(output))

	return str(output)


