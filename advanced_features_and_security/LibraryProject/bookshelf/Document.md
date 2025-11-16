Overview:

This app defines custom model-level permissions: can_view, can_create, can_edit, can_delete on the Book model.
These permissions are enforced in views via @permission_required.
Setup:

Ensure the app “bookshelf” is in INSTALLED_APPS and that django.contrib.auth and django.contrib.contenttypes are also installed.
Run:
python manage.py makemigrations
python manage.py migrate This creates Permission entries for the custom permissions.
Groups:

In Django Admin, create groups such as Viewers, Editors, Admins.
Assign permissions:
Viewers: can_view
Editors: can_view, can_create, can_edit
Admins: can_view, can_create, can_edit, can_delete (and optionally all built-in perms)
Add users to the appropriate groups.
Testing:

Create test users and assign them to the groups.
Log in and attempt to visit:
list_books view: require can_view
add_book view: requires can_create
edit_book view: requires can_edit
delete_book view: requires can_delete
Confirm access is allowed/denied as expected.