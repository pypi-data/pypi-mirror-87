# Django Commons
[![PyPI version](https://badge.fury.io/py/drizm-django-commons.svg)](https://badge.fury.io/py/drizm-django-commons)

This package includes shared code used by
the Drizm organizations development team.  

It is not intended for public usage but you
may still download, redistribute or 
modify it to your liking.

## Installation

Install:  
>pip install drizm-django-commons

Once installed through pip, include
the app in your settings.py like so:  
INSTALLED_APPS += ["drizm_django_commons"]  

In order to use the applications
manage.py commands you must include the
app at the top of the INSTALLED_APPS list.

Import like so:  
import drizm_django_commons

## Documentation

### Custom Management Commands

#### startapp

This version of startapp has been adjust to
play well together with the
Drizm-Django-Template file structure.

Apart from that it is not majorly
divergent from the default commands
functionality.

#### maketest

Automagically creates boilerplate for a
Integration Test for a given application.

## Changelog

### 0.2.1

- Added HrefModelSerializer which will
serialize primary keys to hyperlinks
- Moved testing.py dependencies to
drizm-commons package utilities

### 0.2.2

- Fixed bug with view selection for
SelfHrefField

### 0.3.0

- Rework startapp command for better
default file / folder structure
- Add maketest <app-name> command
to quickly generate boilerplate
for tests
- Integrate DRF-yasg documentation
into Serializer Fields
- Reduced boilerplate and added
additional code comments for
serializer fields
- Add HexColor field
- Fix issue with implicit
view_name retrieval on SelfHrefField
