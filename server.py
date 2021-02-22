# -*- coding: utf-8 -*-
""" VAT validator 9000

SERVER

Handles GET- and POST-requests

Marko Loponen
marko.juhani.loponen@gmail.com
"""
import cherrypy
import json
import os
import re
import db

valid_VAT_pattern = '^[A-Z]{2}[0-9A-Za-z\+\*\.]{2,12}$'
""" Global variable (if we need it somewhere else than in isValid-method)
"""

def isValidFormat(vat):
    """ Check if 'vat' is in right format.
    """
    return re.match(valid_VAT_pattern, vat)
    

@cherrypy.expose
class ValidatorService(object):
    """ Cherrypy server
    """
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def GET(self, var = None):
        """ Handle GET-requests
        
        Return:
            On path /vatApi: Every company information in the database.
            Any other path: Error
        """
        if var == "vatApi":
            return db.listAll()
        
        return {"error": True, "reason": "404", "info": "Path is wrong."}
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def POST(self, var = None):
        """ Handle POST-requests
        
        If path is /vatApi, checks if the message body is in right format and then forward it to Database- and External-modules.
        
        Return: 
            On path /vatApi: Company information based on the given VAT-number.
            Any other path: Error
        """
        
        if var == "vatApi":
            try:
                data = json.loads(cherrypy.request.body.read().decode('utf-8'))
                if 'vat' in data and isValidFormat(data['vat']):
                    return db.is_VAT_valid(data['vat'])
            except:
                pass
            
            return {"city":"","name":"","address":"","postcode":"","updatedOn":"","vatNumber":"","countryCode":"","requestDate":"","error": {"is_error": True, "reason": "Wrong data", "info": "'vat' not found in body or is in wrong format. Check format from documentation."}}
            
        return {"city":"","name":"","address":"","postcode":"","updatedOn":"","vatNumber":"","countryCode":"","requestDate":"","error": {"is_error": True, "reason": "Path", "info": "Path is wrong."}}
        

if __name__ == "__main__":
    """ Cherrypy config and startup.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.sessions.on": True
        },
        "/favicon.ico":
            {
                "tools.staticfile.on": True,
                "tools.staticfile.filename": os.path.join(current_dir, "favicon.ico"),
            }
    }

    cherrypy.config.update(
        {"server.socket_host": "0.0.0.0", "server.socket_port": 6666, 'engine.autoreload.on': False, 'checker.on': False, 'tools.log_headers.on': False,'request.show_tracebacks': False, 'request.show_mismatched_params': False, 'log.screen': False})
    cherrypy.quickstart(ValidatorService(), "/", conf)