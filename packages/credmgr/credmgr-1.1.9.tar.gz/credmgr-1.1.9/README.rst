CredentialManager
=================

Client for interacting with Credential Manager API

-  API version: 1.0
-  Package version: 1.1.9

Requirements
------------

Python 3.6+

Installation & Usage
--------------------

.. code:: sh

    pip install credmgr

Then import the package:

.. code:: python

    from credmgr import CredentialManager

Getting Started
---------------

.. code:: python

    credentialManager = CredentialManager(apiToken='apiToken')

    # List all Reddit apps
    redditApps = credentialManager.redditApps()
    for redditApp in redditApps:
        print(redditApp.name)

    # Create a Reddit app
    redditApp = credentialManager.redditApp.create(name='redditAppName', clientId='clientId', clientSecret='clientSecret', userAgent='userAgent', redirectUri='redirectUri')

    # Get the app by id
    redditApp = credentialManager.redditApp(1)

    # Edit the Reddit app
    redditApp.edit(clientId='clientId2')

    # Delete the app
    redditApp.delete()

