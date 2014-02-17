API
===

This document outlines the basics of Eat Smart Durham's back-end API.


Endpoints
---------

v1 of the API is currently located at: http://107.170.26.176/api/v1/?format=json

There are 3 endpoints:

* `Establishments <http://107.170.26.176/api/v1/establishment/?format=json>`_
* `Inspections <http://107.170.26.176/api/v1/inspection/?format=json>`_
* `Violations <http://107.170.26.176/api/v1/violation/?format=json>`_

The ``format=json`` query string argument is a convenience for viewing within your browser. It's helpful to have a plugin to pretty print JSON, such as `JSONView <https://chrome.google.com/webstore/detail/jsonview/chklaanhfefbnpoihckbnefhakgolnmc?hl=en>`_ for Chrome. Alternatively, you can set the ``Accept: application/json`` header.

Establishment Extras
~~~~~~~~~~~~~~~~~~~~

Establishments are the only entities within the database with geographic elements. To help filtering by these elements, you can use the ``within`` query string argument, such as:

http://107.170.26.176/api/v1/establishment/?format=geojson&est_type=1&ordering=-update_date&within=-78.90999913215637,35.992712509370044,-78.889399766922,35.99845018569175

This will return all restaurants (``est_type=1``) located within a bounding box of downtown Durham.


Example
-------

Let's run through an example with `Watts Grocery
<http://www.wattsgrocery.com/>`_. We can find Watts Grocery by searching on the
``premise_name`` field:

http://107.170.26.176/api/v1/establishment/?premise_name__istartswith=watts%20street%20grocery

This returns 1 result (with an ID of ``57148``) and it's restaurant we're
looking for. You may also notice that the output data is in a format that is
GeoJSON compatible. Since we know the ID now, we can view the detail record:

http://107.170.26.176/api/v1/establishment/57148/

Now we can find it's associated inspections:

http://107.170.26.176/api/v1/inspection/?est_id=57148&order_by=-insp_date&format=json

We only wanted Watts Grocery's inspections, so we specified ``est_id=57148``.
We also ordered by the inspection date (``order_by=-insp_date``) so the latest
inspections would be listed first.

Now we can find all violations for one of the inspections:

http://107.170.26.176/api/v1/violation/?inspection_id=1355101&format=json

That's it!
