import requests
import xml.etree.ElementTree as ET
import db
import server

data_nodes = ["countryCode", "vatNumber", "requestDate", "name", "address"]

namespace = "urn:ec.europa.eu:taxud:vies:services:checkVat:types"

def external_check_VAT(vat):
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
            return {"error": True, "reason": "No VAT", "info":"No company with this VAT exist", "vatNumber": vat}
        company = {}
        
        for node in data_nodes:
            
            if node == "address":
                """ Splitting the address to more prettier.
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