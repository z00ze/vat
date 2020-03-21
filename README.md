# vat
This is a simple python application to get information about company based on a known VAT number.
Cherrypy is handling the requests and information is retrieved from the external service (ec.europa.eu's Vat service) if the vat number is not found in the database. Valid information is saved to the database for faster processing in the future.

MySQL was chosen to store the information as it is widely used, hence this project could easily be maintained in the future. Performance wise, MySQL might be overkill for this project at the start, but should be solid solution for long time while scaling up. In case this API would have 'a lot' requests per seconds, Elastic Search would become feasible solution.

Live API
`https://riski.business/vatApi`

**API**
----

* **URL**

  /vatApi

* **Method:**

  `GET` | `POST` 

* **Data Params**
  
  `POST`<br />
  `Content-Type: application/json`<br />
  `Body: {"vat": <vatnumber>}`<br />
  <br />
  `<vatnumber>` must be in format: `^[A-Z]{2}[0-9A-Za-z\+\*\.]{2,12}$`

* **Success `GET` Response:**

  * **Code:** 200 <br />
    **Content:**   
    ```
    [{
    "city": <city>,
    "name": <name>,
    "error": {
        "is_error": false|true,
        "reason": <error reason>,
        "info": <error info>
    },
    "address": <address>,
    "postcode": <postcode>,
    "updatedOn": <datetime in str when added to database>,
    "vatNumber": <vatnumber>,
    "countryCode": <country code>,
    "requestDate": <date in str when requested from external service>
    }, 
    ...
    ]
    ```

* **Success `POST` Response:**

  * **Code:** 200 <br />
    **Content:**   
    ```
    {
    "city": <city>,
    "name": <name>,
    "error": {
        "is_error": false|true,
        "reason": <error reason>,
        "info": <error info>
    },
    "address": <address>,
    "postcode": <postcode>,
    "updatedOn": <datetime in str when added to database>,
    "vatNumber": <vatnumber>,
    "countryCode": <country code>,
    "requestDate": <date in str when requested from external service>
    }
    ```
 
* **Error Response:**

  * **Code:** 200  <br />
    **Content:** 
    ```
    Error is shown in the response body on the error object. Other fields are empty.
    ...
    "error": {
        "is_error": false|true,
        "reason": <error reason>,
        "info": <error info>
    }
    ...
    ```


* **Sample Calls:**

`GET` all company information which are stored in the database.
```
curl https://riski.business/vatApi
```


`POST` get single company information by VAT number
```
curl -i -X POST -H "Content-Type: application/json" -d "{\"vat\":\"FI21474483\"}" https://riski.business/vatApi
```
  
