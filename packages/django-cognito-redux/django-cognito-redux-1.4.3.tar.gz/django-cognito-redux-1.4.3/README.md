# Django Cognito Authentication

The intent of this library is to provide a package that supports Django and allows an easy implementation for replacing the default Django authentication with an AWS Cognito based authentication.

This is a fork of [Alex Plant](https://github.com/Olorin92)'s great work with the original [django-cognito](https://github.com/Olorin92/django_cognito).

## Install

While this may still work on Django 2.x the focus is going to have it be working on Django 3.x. PRs are welcome as needed for keeping 2.x working.

```
pip install django-cognito-redux
```

## Usage

Need to fill this out more...

Pass in the Access Token and ID Token using headers `ACCESSTOKEN` and `IDTOKEN` respectively. Also pass in the refresh token using using `REFRESHTOKEN`.

## AWS Credentials

This library uses boto3 which follows a specific path for determining what credentials to use. Definitely recommend reading their [Configuring Credentials](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html) section.

    The mechanism in which boto3 looks for credentials is to search through a list of possible locations and stop as soon as it finds credentials. The order in which Boto3 searches for credentials is:

    1. Passing credentials as parameters in the boto.client() method
    2. Passing credentials as parameters when creating a Session object
    3. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`, `AWS_PROFILE`)
    4. Shared credential file (~/.aws/credentials)
    5. AWS config file (~/.aws/config)
    6. Assume Role provider
    7. Boto2 config file (/etc/boto.cfg and ~/.boto)
    8. Instance metadata service on an Amazon EC2 instance that has an IAM role configured.

It is recommended to not pass in arguments with you instantiate a new session or client. Instead use IAM roles for production, and local configuration files locally.

As an example I generally have a profile setup in my `~/.aws/credentials`, and a default region set for that profile in `~/.aws/config`.
From there I set `AWS_PROFILE=profilename` as an environment variable so my app knows what to use. This allows for easy local development as well as
being able to use IAM roles in production, and not having to set a lot of environment variables.

## Recommendations

It is recommended to use a custom user model to set what you need on the model instead of retrofitting existin user model if possible.

## Settings

### COGNITO_USER_MODEL_FIELD_REF_FIELD

Field on your user model you want to use to reference for lookups.

```
COGNITO_USER_MODEL_FIELD_REF_FIELD = 'sub'
```

### COGNITO_TOKEN_REF_FIELD

Field on from the cognito user you want to save as reference to your model

```
COGNITO_TOKEN_REF_FIELD = 'sub'
```

More Examples

```
COGNITO_TOKEN_REF_FIELD = 'sub'
COGNITO_USER_MODEL_FIELD_REF_FIELD = 'sub'

# Is equivilent to

User.objects.get(sub='sub')
```

```
COGNITO_TOKEN_REF_FIELD = 'username'
COGNITO_USER_MODEL_FIELD_REF_FIELD = 'email'

# Is equivilent to

User.objects.get(username='email')
```

### COGNITO_USER_FIELD_MAPPING

The keys of the dictionary map to user fields, and values map to data pulled from the id token. This is used to save data to your user model on create.

```
COGNITO_USER_FIELD_MAPPING = {
    "email": "email",
    "first_name": "custom:first_name",
    "last_name": "custom:last_name",
    "sub": "sub"
}
```

### APP_CLIENT_ID =

The client id of your app client for the user pool

```
APP_CLIENT_ID = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
```

### APP_SECRET_KEY

The secret key for your user pool client

### COGNITO_POOL_ID

The userpool id

```
COGNITO_POOL_ID = 'us-east-1_xxxxxxxxx'
```

### USE_CSRF

```
USE_CSRF = False
```

### HTTP_ONLY_COOKIE

```
HTTP_ONLY_COOKIE = False
```

### SECURE_COOKIE

```
SECURE_COOKIE = False
```

### AUTO_CREATE_USER

Create a user if tokens validate if the user doesn't exist.

```
AUTO_CREATE_USER = True
```

## Changelog

### 1.4.3

- Change django-rest-framework depdencies to be more inclusive.

### 1.4.1

- Upgrade depdencies to be in sync for Django 3.0

### 1.4.0

- Change token validation to validate ID Tokens and Access Tokens
- Add settings for mapping attributes from the ID Token to the user model
- Change token use to be an ID Token instead of Access Token
- Added more Docs
- Cover race condition where someone might call backend more than once before user is created
