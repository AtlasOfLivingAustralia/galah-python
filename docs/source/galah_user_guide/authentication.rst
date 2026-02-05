.. _Authentication:

Authentication (Experimental)
================================

The ALA has been improving its security measures recently, and that comes with the 
ability to log into the ALA programmatically to get data.  What this means for the 
user is not only the ability to create more complex queries, it means that users 
with authorisation can get exact locations of species that are otherwise obfuscated 
to the general public.  To find out more information about becoming one of those 
users, `contact us <mailto:support@ala.org.au>`_.

Option 1 (Recommended): Browser
-----------------------------------

``galah-python``'s default option for authentication is to launch your browser so 
you can log into the ALA, and ``galah-python`` will parse and store what you need 
for authentication in your configuration file.  All you have to do for this is 
use the ``galah.galah_config()`` command.

.. prompt:: Python

    >>> import galah
    >>> galah.galah_config(authenticate=True)

This will open up your browser, and you will be prompted to log into your ALA account.

After you log in, close the browser and continue coding.  All the relevant authentication 
information is stored in your configuration file.  

If this information becomes out of date, ``galah-python`` will automatically refresh your 
token, though you may be prompted to log in again

Option 2: Download Tokens Manually
-------------------------------------

For those who cannot use the browser, there is a second option.  You can `contact us <mailto:support@ala.org.au>`_ 
to get yourself a client id for our system.  When you get an email back with your client id, go to 
`ALA tokens <tokens.ala.org.au>`_ 
site and enter your client id.  You will then press "Next" and then "Generate Token".  Download the ``auth.json`` and use this 
as an argument to the ``galah.galah_config()``

.. prompt:: Python

    >>> import galah
    >>> galah.galah_config(authenticate=True,auth_filename='auth.json')

Like above, the authentication information will be stored in the configuration file.