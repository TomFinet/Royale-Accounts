import random
import string


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_order_id_generator(instance, new_slug=None):
	new_order_id = random_string_generator()

	Klass = instance.__class__
	qs_exists = Klass.objects.filter(order_id=new_order_id).exists()
	if qs_exists:
		return unique_order_id_generator(instance)
	return new_order_id

def unique_token_generator(instance):
    new_token = random_string_generator(50)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(token=new_token).exists()
    if qs_exists:
        return unique_token_generator(instance)
    return new_token

def unique_slug_generator(instance, _from=-1, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        if _from == 0:
            slug = '{arena}-level-{king_tower}'.format(
                arena=instance.get_slug_arena().lower(), 
                king_tower=instance.king_tower
            )
        elif _from == 1:
            slug = '{title}'.format(
            title=instance.get_slug_title().lower(), 
        )
        else:
            slug = None

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
    