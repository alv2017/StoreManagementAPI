# STORE MANAGEMENT API

### Intro

Store Management API is designed for programmatic e-store management.
Currently, it supports product management and order status management functions.
Please note that the person responsible for online store management, does not
have access to order update/delete options. He/She can only preview orders,
and update order status, to keep the customers informed about their orders.


Products API:
   - Product listing;
   - Product details preview;  
   - Addition of new products;
   - Update of existing products;
   - Deletion of redundant products;
   - Update of product stock;

Orders API:
   - Order listing;
   - Order details preview;
   - Order status history preview;
   - Order status preview, update, and deletion.

   

At the moment Store Management API supports the following authentications methods:
   1) Session authentication: It is used when working with Browsable API.
      Browsable API is provided for convenience to test the API functionality.
   2) Basic Authentication: It is used when working the actual API.


The Store Management API is in its early development stage, in order to check
its functionality just download the project, install the project dependencies,
and simply start the development server by issuing the command:

    $ python manage.py runserver_plus --cert-file cert.crt

Click on the entry link or enter it to the browser window 
(if you are running the project on localhost: https://127.0.0.1:8000/),
and you will find yourself at the Store Mangement API entry page.
The entry page was created using DjangoREST browsable API, I tried to make it intuitive to navigate
and explore the API.

### OpenAPI Schema

If you run the project from the local machine using the default options, then browsable API
can be found at: [https://127.0.0.1:8000/schema/](https://127.0.0.1:8000/schema/)


### Login Credentials

In order to use the API you need to provide login credentials. At the moment
the following login credentials has been set:

  - User: **admin**, Password: **admin123**, Access: everything, including Django-Admin
   
  - User: **regular_user**, Password: **good-day**, Access: index page and API schema.

  - User: **anonymous**, Password: , Access: index page and API schema.
   
  - User: **staff_member**, Password: **good-day**, Access: All the API endpoints
   
  - User: **store_admin**, Password: **good-day**, Access: All the API endpoints

All in all, in order to use API you need to log in (if you are using Browsable API),
or you need to provide the user credentials when sending requests to the API.

### Browsable API

The project supports browsable API functionality, so if you find yourself
in trouble, just type the endpoints urls directly into your browser, 
and use the API from GUI.

### Running Tests

Good news: You do not need to provide any user credentials when running test.

All you need to do is to sit back and issue the command:

    $ pytest -v

