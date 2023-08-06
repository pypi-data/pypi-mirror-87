# django-allauth-d120
django-allauth-d120 is a provider for [allauth](https://www.intenct.nl/projects/django-allauth/) to integrate d120
 accounts into django projects. It therefor provides a wrapper around the allauth OAuth 2.0 provider and connects it 
 with the [keycloak](https://www.keycloak.org/) OAuth 2.0 endpoint. The app allows to synchronize the groups of a
 user from keycloak to your django project.

## Installation
1. Install django-allauth-d120 with pip e.g. `pip install django-allauth-d120`
2. Add the following apps to the installed `INSTALLED_APPS` in the `settings.py`:  
`'django.contrib.sites',`  
`'allauth',`  
`'allauth.account',`  
`'allauth.socialaccount',`  
`'allauth_d120_provider',`  
3. Configure the Authentication backends in the `settings.py`:
```python
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)
```
4. Configure allauth to disable email verification, account sing up outside the sso and 
account sign up via the sso in the `settings.py`:
```python
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_ADAPTER = "allauth_d120_provider.account_adapter.DisableSignUpAdapter"
SOCIALACCOUNT_ADAPTER = "allauth_d120_provider.account_adapter.SocialAccountAdapter"
```
5. Run `manage.py migrate` to create sync the database with the newly installed apps
6. Login into the Django Admin webinterface to configure the website object. Therefore go to site section and 
select the site model e.g. the url ends on `admin/sites/site/` where `admin/` is the root path of Django Admin
 in your project. Make sure the domain matches the domain your project is running on.
7. Within Django Admin go to the Social Accounts section and select the Social applications model e.g. the url 
ends on `admin/socialaccount/socialapp/` where `admin/` is the root path of Django Admin in your project. 
Add a new instance which uses `D120 OAuth 2.0` as provider. Please ask fss@ for a Client id and the related Secret Key.
8. Have a look at the [instructions to install allauth](https://django-allauth.readthedocs.io/en/latest/installation.html). 
There might be steps necessary steps that are not mentioned in this instruction.
## Group Synchronization
You can create a group synchronization by adding instances of the groupsync Model via Django Admin. 
Therefor select the Group Synchronization model in the D120 Autentication Provider section. 
The groups synchronize when the user logs into the project.