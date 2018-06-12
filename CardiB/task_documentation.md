# Description
1. CarDB is a database interface
2. Models are defined in cardb/types.py
3. Instruction creating empty tables car and brand is in cardb/types.py (run the script)
4. CarDB is in cardb/cardb.py .
5. CarDB methods are:

    * create_brand()
    * delete_brand()
    * query_brands()

    * create_car()
    * delete_car()
    * update_car()
    * query_cars()
    REST API uses those methods
    Function update_brands() was not implemented, because of Foreign Key limitations
6. REST API is in app.py and is written in Flask
7. Interface uses  SQLAlchemy
8. Full access to REST API is ensured by logging in using flask.session
9. Use RESTer albo POSTman to use request methods other than GET
10. Several tests were written and run testing CarDB methods

# Endpoints and request methods for REST API:

### `/`
* **GET**
    The usual Hello World response, app's test

### `/login`
* **POST**
    Logging in, necessary login data is available in app.py

* **GET**
    Instructions how to log in

### `/logout`
* **POST**
    Logging out

### `/cars`
* **GET**
    Only logged in users have access, otherwise will be redirected to `/login`.
    Cars from table car in database are returned.
    One can filter the results:

    `/cars?brand=Audi`
    All cars whose brand is Audi

    `/cars?id=4`
    A car whose id=4

    `/cars?model=A5`
    All cars whose model is A5

    
    `cars?info={"first_production_year": 1996}`
    All cars that were released first in 1996


* **POST**
    Posts (adds) a new car to the database. A check is performed whether the brand (brand column value) of the car exists in table brand. Otherwise such car will not be added.
    Data format:
    ```json
  {
      "brand": "Audi",
      "model": "A4",
      "info": {
          "engine": "diesel",
          "production_year": 2009
      }
           
  }
  ```

* **DELETE**
    Will delete a car whose id will be specified in query string
    Example: `/cars?id=3` will delete car whose id=3, provided it exists


* **PATCH**
    Changes car's data. 
    If we are to change car brand, function performs a check if such brand exists in brand table. No changes will be made if not.
    Car's id is specified in query string.
    Example: `/cars?id=3` 
    Data format:

      ```json
  {
      "brand": "Volkswagen",
      "model": "Golf",
      "info": {
          "production_year": 2010
      }
           
  }
  ```
  Columns' 'brand', 'model', 'info' values will be changed in a car whose id=3
  Why did I use PATCH not PUT? Well, you can use PATCH and replace all columns or you can PATCH only one or two Therefore it seemed more practical to use PATCH.

### `/brands`
* **GET**
    A list of all brands is returned
    Results can be filtered:

    `/brands?id=5`
    Brand whose id=5 will be returned

   `/brands?name=Audi`
   Will return name of the brand, provided it exists in the database

* **POST**
    Adds a brand to the database. Function performs a check if such brand already exists, if so it will not be added.
    Data format:

    ```json
  {
      "name": "Your_brand_goes_here"
           
  }
  ```

* **DELETE**
    Will delete a record in table brands provided that in 'car' table no cars of such brands exist. If they do, warning is issued, no brand is deleted
    Example: `/brands?id=3` might delete brand whose id=3 if abovementioned conditions are met.


