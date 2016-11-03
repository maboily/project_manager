from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response


# Create your views here.


def home(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            login(request, form.get_user())

            return HttpResponseRedirect('/projects/')
    else:
        form = AuthenticationForm()

    return render_to_response('login.html', {'form': form})


@login_required
def projects(request):
    return render_to_response('projects/index.html')
