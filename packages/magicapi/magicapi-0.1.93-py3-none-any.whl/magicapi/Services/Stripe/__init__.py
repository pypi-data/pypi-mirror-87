import stripe
from magicapi import settings

stripe.api_key = settings.stripe_api_key
