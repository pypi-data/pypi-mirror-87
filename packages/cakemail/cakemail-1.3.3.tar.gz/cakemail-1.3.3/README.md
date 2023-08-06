# Install

Install the `cakemail` package using `pip`

```shell script
pip install cakemail
```

# Usage

Create an object from the `CakemailApi` class with your Cakemail username and password.  The object will take care of
all authorization mechanisms automatically.

```python
import cakemail

api = cakemail.Api(username='your@email.com', password='somepassword')
```

Call one of the API operations (refer to the online documentation)

```python
my_account = api.account.get_self()
```

# API operations

API operations accept the OpenAPI models as well as python dictionaries.

```python
from cakemail.models import CreateSender

sender = api.sender.create(
    create_sender=CreateSender(
        name='My Sender',
        email='someone@gmail.com'
    )
)
sender = api.sender.create(
    create_sender={
        'name': 'My Sender',
        'email': 'someone@gmail.com'    
    }
)
```

You can also unpack a dictionary for all Operation arguments, allowing you to express the entire payload as a single
dictionary :

```python
sender = api.sender.create(
    **{
        'create_sender': {
            'name': 'My Sender',
            'email': 'someone@gmail.com'        
        }   
    }
)
```

# Operation Examples

## Create a Sender
```python
from cakemail.models import CreateSender, ConfirmSender

sender = api.sender.create(
    CreateSender(name='My Sender', email='someone@gmail.com')
)

# look for the confirmation ID in your email inbox
api.sender.confirm(
    ConfirmSender(confirmation_id='[confirmation ID]')
)
```

## Create a Contact List

```python
from cakemail.models import List, Sender

my_new_list = api.list.create(
    list=List(
        name='my new list',
        default_sender=Sender(id=sender.id)
    )
)
```

## Send a transactional email

```python
from cakemail.models import Email, EmailContent

# expressed as OpenAPI models
api.transactional_email.send(
    email=Email(
        email='destination@gmail.com',
        sender=sender,
        content=EmailContent(
            subject='Subject line',
            text='Email body',
            encoding='utf-8'
        )
    )
)

# expressed as a dictionary
api.transactional_email.send(
    email={
        'email': 'destination@gmail.com',
        'sender': sender,
        'content': {
            'subject': 'Subject line',
            'text': 'Email body',
            'encoding': 'utf-8' 
        }
    }
)
```

## Accessing data

The CakemailAPI always return its data under the `data` object.  For simplicity, the resource data is accessible
from the returned response directly:

```python
my_user = api.user.get_self()

print(f'id: {my_user.id}, email: {my_user.email}')

```
## Iterate through lists

Some methods return a list of resources on which you can iterate directly:

```python
campaigns = api.campaign.list()
for campaign in campaigns:
    html = api.campaign.render(campaign_id=campaign.id).html
    print(f'id: {campaign.id}, name: {campaign.name}, html: {html}')

```

## Pagination

Pagination is stored in the `pagination` property of all methods returning a list of resources:

```python
campaigns = api.campaign.list(with_count=True)

print(f"""
  page: {campaigns.pagination.page},
  per_page: {campaigns.pagination.per_page},
  count: {campaigns.pagination.count}
  """)
```

## Dictionary representation

The API methods return response objects; if you prefer to work with a python dict representation, use the `to_dict` method:

```python
campaign_dict = api.campaign.get(campaign_id=123).to_dict()

for campaign in api.campaign.list():
    print(campaign.to_dict())
```
