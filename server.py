# -*- coding: utf-8 -*-
""" VAT validator 9000

Marko Loponen
marko.juhani.loponen@gmail.com
"""

import os
import cherrypy

@cherrypy.expose
class ValidatorServvice(object):
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def GET(self, var = None):
        if(var == 'vat_list'):
            return "uWu"
        return "Nothing here.... Carry on Wayward Son."

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True
        },
        '/favicon.ico':
            {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': os.path.join(current_dir, 'favicon.ico'),
            }
    }

    cherrypy.config.update(
        {'server.socket_host': '0.0.0.0', 'server.socket_port': 6666, })
    cherrypy.quickstart(ValidatorServvice(), '/', conf)