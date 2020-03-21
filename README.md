# vat



**API**
----
  This is simple API to retvieve company information based on a known VAT number.

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
  
