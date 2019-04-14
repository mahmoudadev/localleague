from django.utils.functional import wraps
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden


def check_team_leader(view):
    @wraps(view)
    def inner(request, *args, **kwargs):
        # Check and see if the logged in user is team leader
        if not request.user.user_type == 'team_leader':
            if request.user.is_superuser:
                pass
            else:
                return render(request, 'forbidden.html')

        # Return the actual object to the view
        return view(request, *args, **kwargs)

    return inner


def check_team_player(view):
    @wraps(view)
    def inner(request, *args, **kwargs):
        # Check and see if the logged in user is team player
        if not request.user.user_type == 'player':
            if request.user.is_superuser:
                pass
            else:
                return render(request, 'forbidden.html')

        # Return the actual team object to the view
        return view(request, *args, **kwargs)

    return inner

def check_team_leader_or_player(view):
    @wraps(view)
    def inner(request, *args, **kwargs):
        # Check and see if the logged in user is team player
        if not ( request.user.user_type == 'player' or request.user.user_type == 'team_leader'):
            if request.user.is_superuser:
                pass
            else:
                return render(request, 'forbidden.html')

        # Return the actual team object to the view
        return view(request, *args, **kwargs)

    return inner

def check_sponsor(view):
    @wraps(view)
    def inner(request, *args, **kwargs):
        # Check and see if the logged in user is sponsor
        if not request.user.user_type == 'sponsor':
            if request.user.is_superuser:
                pass
            else:
                return render(request, 'forbidden.html')

        # Return the actual object to the view
        return view(request, *args, **kwargs)

    return inner


def check_landlord(view):
    @wraps(view)
    def inner(request, *args, **kwargs):
        # Check and see if the logged in user is landlord
        if not request.user.user_type == 'landlord':
            if request.user.is_superuser:
                pass
            else:
                return render(request, 'forbidden.html')

        # Return the actual object to the view
        return view(request, *args, **kwargs)

    return inner


def check_admin(view):
    @wraps(view)
    def inner(request, *args, **kwargs):
        # Check and see if the logged in user is superuser (admin)

        if not request.user.is_superuser:
            return render(request, 'forbidden.html')

        # Return the actual object to the view
        return view(request, *args, **kwargs)

    return inner
