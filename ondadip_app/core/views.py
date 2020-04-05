from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from numpy import setdiff1d
from .models import Security, User, UserPortfolio


class IndexView(generic.ListView):
    template_name = 'core/index.html'
    context_object_name = 'latest_securities_list'

    def get_queryset(self):
        """Return the last five created securities"""
        return Security.objects.order_by('-created_at')[:5]


class UserView(generic.DetailView):
    model = User
    template_name = 'core/user.html'


class SecurityView(generic.DetailView):
    template_name = 'core/security.html'
    model = Security


class PortfolioView(generic.DetailView):
    template_name = 'core/portfolio.html'
    model = User

    def get_context_data(self, **kwargs):
        """Overriden to add `portfolio` to the template context."""
        context = super().get_context_data(**kwargs)
        all_securities = Security.objects.all()
        existing_securities = context['user'].portfolio_security.all()

        securities_symbols_final = setdiff1d(
            [e.symbol for e in all_securities],
            [e.security.symbol for e in existing_securities],
            assume_unique=False
        ).tolist()

        securities = Security.objects.filter(symbol__in=securities_symbols_final)

        context['securities'] = securities
        return context


class SecurityAddedView(generic.DetailView):
    model = User
    template_name = 'core/security_added.html'


def security_add(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    try:
        selected_security = Security.objects.get(pk=int(request.POST['security']))
    except (KeyError, UserPortfolio.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'core/portfolio.html', {
            'error_message': "You didn't select a security.",
        })
    else:
        user.add_to_portfolio(selected_security)
        print("Added " + selected_security.symbol)
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('core:security_added', args=(user.id,)))
