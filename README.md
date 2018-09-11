# django_sample

A short but exemplary Django project, with these features:

* Works with Python 3.5.2 and Django 2.1.1
* Uses djangorestframework 3.8.2
* Uses django-extensions 2.1.2, pygraphviz 1.3.1, and graphviz 2.38.0 to draw an ERM diagram
* Uses Sqlite3 for a conveniently simple back-end
* Links Django's standard User model to many Account models
* Links many Account models to one RiskType model, simulating an insurance system
* Links one RiskType model to many CustomField models, to define extra data for each account
* Links many CustomValue models to one Account and one CustomField, to contain the extra data itself
* Specializes CustomValues into Addresses, Currencies, Enums, PhoneNumbers, and Strings
* Displays, edits, and validates CustomValues with the Flyweight Design Pattern
* Serves a JSON list of RiskTypes at the REST endpoint api/v1/risk_types
* Serves one RiskType at the REST endpoint api/v1/risk_types/99
* Tests all of the above with Python's unittest. (A real project would test the views & JavaScript, too!)
* Serves a list of Users, Accounts, and CustomValues in HTML at the home page /
* Expands and collapses that list with Vue.js
