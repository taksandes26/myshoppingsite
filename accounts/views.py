from django.shortcuts import render, reverse
from django.contrib.auth import views as auth_views, authenticate, login, logout
from django.views.generic import View
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from .models import Profile
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class SignUpView(View):
    from_class = SignUpForm
    initial_template = 'registration/register.html'
    template_name = 'registration/registration_done.html'

    def get(self, request):
        user_form = self.from_class()
        return render(request, self.initial_template, {'user_form': user_form})

    def post(self, request):
        form = self.from_class(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)  # created new_user object avoid saving it yet
            password = form.cleaned_data.get('password1')  # set the chosen password
            new_user.set_password(password)
            new_user.save()
            messages.success(request, "user registered")
            return render(request, self.template_name, context={'new_user': new_user})
        else:
            messages.error(request, "Form has error, please check")
            return render(request, self.initial_template)


class LoginView(View):
    form_class = LoginForm
    template_name = 'registration/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('accounts:dashboard'))

                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse("invalid user")
        else:
            form = LoginForm()
            return render(request, self.template_name, {'form': form})


class DashboardView(View):
    template_name = 'accounts/dashboard.html'

    @method_decorator(login_required)
    def get(self, request):
        if True:
            messages.success(request, "welcome to dashboard")
        messages.error(request, "Error", extra_tags="alert alert-success")
        return render(self.request, self.template_name, {})


class LogoutView(View):
    template_name = 'registration/logout.html'

    @method_decorator(login_required())
    def get(self, request):
        logout(request)
        return render(self.request, self.template_name)