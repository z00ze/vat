# -*- coding: utf-8 -*-
""" VAT validator 9000

EXTERNAL

Handles SOAP-request to external validation service and formatting data into simple format.

Marko Loponen
marko.juhani.loponen@gmail.com
"""
import xml.etree.ElementTree as ET
import requests
import server
import db


data_nodes = ["countryCode", "vatNumber", "requestDate", "name", "address"]
""" Data field names of the external service.
"""

namespace = "urn:ec.europa.eu:taxud:vies:services:checkVat:types"

def external_check_VAT(vat):
    """ Check VAT from ec.europa.eu's Vat service.
    
    Parameters:
        vat (str) : Company VAT number
    
    Return:
    SUCCESS:
        (dict) : Company data in format:
                "city": str,
                "name": str,
                "address": str,
                "postcode": str,
                "updatedOn": datetime in str when added to DB,
                "vatNumber": str,
                "countryCode": str,
                "requestDate": date in str when requested from external service
    FAILURE:
        (dict) : 
    """
    url='http://ec.europa.eu/taxation_customs/vies/services/checkVatService'
    headers = {'content-type': 'application/soap+xml'}
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:ec.europa.eu:taxud:vies:services:checkVat:types">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:checkVat>
         <urn:countryCode>"""+vat[0:2]+"""</urn:countryCode>
         <urn:vatNumber>"""+vat[2:]+"""</urn:vatNumber>
      </urn:checkVat>
   </soapenv:Body>
</soapenv:Envelope>"""
    
    response = (requests.post(url,data=body,headers=headers),)[0]

    if response.status_code == 200:
        
        root = ET.fromstring(response.text)
        
        if root.find(".//{" + namespace + "}valid").text == "false":
            return {"city":"","name":"","address":"","postcode":"","updatedOn":"","vatNumber":"","countryCode":"","requestDate":"","error": {"is_error": True, "reason": "No VAT", "info": "No company with this VAT exist"}}
        
        company = {"error": {"is_error": False, "reason": "", "info": ""}}
        
        for node in data_nodes:
            
            if node == "address":
                """ Splitting the address to postcode and city.
                """
                temp = root.find(".//{" + namespace + "}"+node).text.split("\n")
                if len(temp) == 2:
                    company[node] = temp[0]
                    
                    temp2 = temp[1].split(" ")
                    if len(temp2) >= 2:
                        company["postcode"] = temp2[0]
                        company["city"] = " ".join(temp2[1:])
            else:
                company[node] = root.find(".//{" + namespace + "}" + node).text
        
        if not server.isValidFormat(company['vatNumber']):
            company['vatNumber'] = vat
            
        db.insertNewCompany(company)
        return company
    return False