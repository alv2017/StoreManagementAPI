# PRODUCT MANAGEMENT API

### Intro

Product Management API is designed for programmatic e-store products management.
Currently it supports the following functions:
   - Listing of available products;
   - Adding of new products;
   - Update of existing products;
   - Deletion of redundant products;
   - Update of product stock;

At the moment Product Management API supports the following authentications methods:
   1) Session authentication: It is used when working with Browsable API.
      Browsable API is provided for convenience to test the API functionality.
   2) Basic Authentication: It is used when working the actual API.


The Product Management API is in its early development stage, in order to check
its functionality just download the project, install the project dependencies,
and simply start the development server by issuing the command:

    $ python manage.py runserver_plus --cert-file cert.crt

Click on the entry link or enter it to the browser window 
(if you are running the project on localhost: https://127.0.0.1:8000/),
and you will find yourself at the Product Management
API documentation page. Here you will find all the information needed to 
use the API.

### Login Credentials

In order to use the API you need to provide login credentials. At the moment
the following login credentials has been set:

1) User: admin, Password: admin123, Access: everything, including Django-Admin
   
2) User: regular_user, Password: good-day, Access: index page with API documentation
   
3) User: staff_member, Password: good-day, Access: All the API endpoints
   
4) User: store_admin, Password: good-day, Access: All the API endpoints

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

