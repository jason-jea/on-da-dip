from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Security, User, UserPortfolio


def index(request):
    latest_securities_list = Security.objects.order_by('-created_at')[:5]

    context = {
        'latest_securities_list': latest_securities_list,
    }

    return render(request, 'core/index.html', context)


def user(request, user_id):
    user = User.objects.get(pk=user_id)

    return render(request, 'core/user.html', {'user': user})


def security(request, security_id):
    security = get_object_or_404(Security, pk=security_id)

    return render(request, 'core/security.html', {'security': security})


def portfolio(request, user_id):
    user = User.objects.get(pk=user_id)
    portfolio_securities_list = user.portfolio_security.all()
    context = {
        'portfolio_securities_list': portfolio_securities_list,
        'user': user,
    }
    return render(request, 'core/portfolio.html', context)
