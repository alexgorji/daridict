from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import UserRegistrationForm
from helpers.classes import LoginAndPermissionRequiredMixin

from .forms import ProfileRegistrationForm
from .models import Profile


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            if profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                return render(request, 'profiles/register_done.html', context={'profile': profile})
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileRegistrationForm()
    return render(request, 'profiles/register.html', context={'user_form': user_form, 'profile_form': profile_form})


class ProfileDetailView(LoginAndPermissionRequiredMixin, generic.DetailView):
    model = Profile
    permissions = ('profiles.view_profile',)


class ProfileUpdateView(LoginAndPermissionRequiredMixin, generic.UpdateView):
    model = Profile
    fields = ['first_name', 'last_name', 'tax_id_number']
    template_name_suffix = '_update_form'
    permissions = ('profiles.change_profile',)

    def post(self, request, *args, **kwargs):
        if 'profile_update_cancel' in request.POST:
            return redirect(self.get_object().get_absolute_url())
        elif 'profile_delete' in request.POST:
            return redirect(reverse_lazy('profiles_delete', kwargs={'pk': self.get_object().id}))
        return super().post(self, request, *args, **kwargs)


class ProfileDeleteView(LoginAndPermissionRequiredMixin, generic.DeleteView):
    model = Profile
    success_url = reverse_lazy('home')
    permissions = ('profiles.delete_profile',)
