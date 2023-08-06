Changelogs
==========

Changelogs is, as the name implies, a changelog app to keep track of your application's version.


Quick start
-----------

1. Add "changelogs" to your INSTALLED_APPS setting like this:

    ```
    INSTALLED_APPS = [
    ...
    'changelogs',
    ]
    ```

2. Run ``python manage.py migrate`` to create necessary models.

3. Start the development server and visit http://127.0.0.1:8000/admin/changelogs/
   to create a changelog version (you'll need the Admin app enabled).

