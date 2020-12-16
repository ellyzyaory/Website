from .models import Checkout

# id generator for checkout
def id_generator(size= 10, chars = string.ascii_uppercase + string.digits):
    the_id =  "".join(random.choice(chars) for x in range(size))
    # object exist
    try:
        checkout = Checkout.objects.get(checkout_id= the_id)
        id_generator()
    # object does not exist
    except Checkout.DoesNotExist:
        return the_id
