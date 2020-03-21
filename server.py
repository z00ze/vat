# -*- coding: utf-8 -*-
""" VAT validator 9000

Marko Loponen
marko.juhani.loponen@gmail.com
"""

import os
import json
import cherrypy
import re

import db

valid_VAT_pattern = '^[A-Z]{2}[0-9A-Za-z\+\*\.]{2,12}$'
""" Global variable (if we need it somewhere else than in isValid-method)
"""

def isValidFormat(vat):
    return re.match(valid_VAT_pattern, vat)
    

@cherrypy.expose
class ValidatorService(object):
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def GET(self, var = None):
        
        if var == "checkVat":
            return db.listAll()
        
        return "Nothing here..."
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def POST(self, var = None):
        
        if var == "checkVat":
            data = json.loads(cherrypy.request.body.read().decode('utf-8'))
            if 'vat' in data and isValidFormat(data['vat']):
                """ Initial regex check if the VAT is valid.
                """
                return db.is_VAT_valid(data['vat'])
            
        
        return "Nothing here..."
        
            
    
        


if __name__ == "__main__":
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
        {"server.socket_host": "0.0.0.0", "server.socket_port": 6666, })
    cherrypy.quickstart(ValidatorService(), "/", conf)