- Alpha release
- Works for make a payment
Usage:

from .pyflow.client import Client

client = Client(
                'flow_api_key',
                'flow_private_key',
		'flow_enviroment_url',
		True, #test Mode
            )

post = {
	    'email': 'testclient@test.tld',
	    'amount': 500,
	    'commerceOrder': 'code_comerce',
            'subject': 'so1',
            'paymentMethod': 9,
            'urlConfirmation': 'url.tld/confirm',
            'urlReturn': 'url.tld/return',

       }

client.payments.post(post)
