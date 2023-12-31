from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from news.models import Author
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'account/account.html'
    form_class = UserCreationForm

    def get_object(self, **kwargs):
        username = self.request.user.username
        return User.objects.get(username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not Author.objects.filter(user=self.get_object()).exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    if not Author.objects.filter(user=user).exists():
        Author.objects.create(user=user)
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')
    return redirect('/')
