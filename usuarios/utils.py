from django.contrib.auth.models import Group


def assign_superuser_group(user):

    superuser_group, created = Group.objects.get_or_create(name='Superusuário')


    if not user.groups.filter(name='Superusuário').exists():
        user.groups.add(superuser_group)


def assign_limited_group(user):

    limited_group, created = Group.objects.get_or_create(name='Usuário Comum')


    if not user.groups.filter(name='Usuário Comum').exists():
        user.groups.add(limited_group)
