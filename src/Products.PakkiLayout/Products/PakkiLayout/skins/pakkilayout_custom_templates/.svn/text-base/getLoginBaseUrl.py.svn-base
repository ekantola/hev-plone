## Script (Python) "getLoginBaseUrl"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Return the base url for logging in, taking https into account
portal_url = context.absolute_url()

# Force HTTPS for login for the following base urls
NEEDS_HTTPS = [
    'http://www.papa.partio.fi',
    'http://pakki.papa.partio.fi',
    'http://pakki-dev.papa.partio.fi',
]

if portal_url in NEEDS_HTTPS:
    portal_url = portal_url.replace('http://', 'https://')

return portal_url
