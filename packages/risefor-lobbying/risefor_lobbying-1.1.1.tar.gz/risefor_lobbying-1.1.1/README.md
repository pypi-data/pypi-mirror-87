
# Synopsis

Risefor-Lobbying is a package for DjangoLDP that provides the models and behaviour to run a site which manages public lobbying initiatives. Allowing you to federate with other providers to achieve the maximum users for lobbying government

# Requirements

* Python 3.6
* Django (known to work with Django 1.11)
* DjangoLDP
* Django Rest Framework
* pyld
* django-guardian
* djangorestframework-guardian

# Installation

1. Install DjangoLDP
TODO

2. Install Sib-Manager CLI
TODO

3. Add as a package
TODO

4. Install package
TODO

## User model requirements

When implementing authentication in your own application, you have two options:

* Using or extending [DjangoLDP-Account](https://git.startinblox.com/djangoldp-packages/djangoldp-account), a DjangoLDP package modelling federated users
* Using your own user model & defining the authentication behaviour yourself

Please see the [Authentication guide](https://git.startinblox.com/djangoldp-packages/djangoldp/wikis/guides/authentication) for full information

If you're going to use your own model then your user model must extend `DjangoLDP.Model`, or define a `urlid` field on the user model, for example:
```python
urlid = LDPUrlField(blank=True, null=True, unique=True)
```

The `urlid` field is used to uniquely identify the user and is part of the Linked Data Protocol standard. For local users it can be generated at runtime, but for some resources which are from distant servers this is required to be stored

# Testing

Packaged with Risefor-Lobbying is a tests module, containing unit tests

You can extend these tests and add your own test cases by following the examples in the code. You can then run your tests with:
`python -m unittest tests.runner`