from django.contrib.auth.models import Group


def save_to_group(backend, user, response, *args, **kwargs):
    '''
    pipline for adding a new user to necessary group
    '''
    payer_group = Group.objects.get(name='Payers')
    user.groups.add(payer_group)
