from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from numpy import setdiff1d
from .models import Security, User, UserPortfolio


class IndexView(generic.ListView):
    """homepage lists latest 5 securities by created date"""
    template_name = 'core/index.html'
    context_object_name = 'latest_securities_list'

    def get_queryset(self):
        """Return the last five created securities"""
        return Security.objects.order_by('-created_at')[:5]


class UserView(generic.DetailView):
    # subclassing Django's generic detail view (returns details of a model object)
    # this is a view that returns details about a user
    model = User
    template_name = 'core/user.html'


class SecurityView(generic.DetailView):
    """returns details about a security"""
    template_name = 'core/security.html'
    model = Security


class PortfolioView(generic.DetailView):
    """returns details about a user's portfolio"""
    template_name = 'core/portfolio.html'
    model = User

    def get_context_data(self, **kwargs):
        """Override default to add a list of available securities for the user to the template context."""
        context = super().get_context_data(**kwargs) # this grabs the existing context for this view (just the user object)
        all_securities = Security.objects.all()
        existing_securities = context['user'].portfolio_security.all()

        # using set logic, return items from set1 that don't exist in set2
        # this is the same as a left join filtering where left_table.id is null
        securities_symbols_final = setdiff1d(
            [e.symbol for e in all_securities],
            [e.security.symbol for e in existing_securities],
            assume_unique=False
        ).tolist()

        securities = Security.objects.filter(symbol__in=securities_symbols_final)

        context['securities'] = securities
        return context


class SecurityAddedView(generic.DetailView):
    """Results page after adding a security."""
    model = User
    template_name = 'core/security_added.html'


def security_add(request, user_id):
    """Method for adding a security through a form to a user's portfolio."""
    # this is the manual way of retrieving the relevant object through a GET request
    user = get_object_or_404(User, pk=user_id)
    try:
        # when user hits 'add' button, request.POST returns a dictionary
        # in this case just one entry 'security' (security.id to be more specific)
        selected_security = Security.objects.get(pk=int(request.POST['security']))
    except (KeyError, UserPortfolio.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'core/portfolio.html', {
            'user': user,
            'error_message': "You didn't select a security.",
        })
    else:
        user.add_to_portfolio(selected_security)
        print("Added " + selected_security.symbol)
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('core:security_added', args=(user.id,)))
