from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Tweet, Follow
from django.views.generic import DetailView
from django.contrib.auth.models import User
from .forms import TweetForm
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


class UserView(DetailView):
    model = User
    template_name = 'home.html'

    def get_object(self):
        return self.get_queryset().get(username=self.kwargs['username'])


@login_required
def tweet_new(request):
    if request.method == "POST":
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.author = request.user
            tweet.created_at = timezone.now()
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_edit.html', {'form': form})


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def tweet_list(request):
    tweets = Tweet.objects.filter(created_at__lte=timezone.now()).order_by('-created_at')
    # follow = Follow.objects.get(created_at__lte=timezone.now(), author__id=pk).order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})


def user_profile(request, pk):
    tweets = Tweet.objects.filter(created_at__lte=timezone.now(), author__id=pk).order_by('-created_at')
    return render(request, 'user_profile.html', {'tweets': tweets,
                                                 'pk': pk})


def follow(request, pk, pk2):
    f = Follow(user=User.objects.get(id=pk), target=User.objects.get(id=pk2))
    try:
        f.save()
        return JsonResponse({"Success": True})
    except Exception as e:
        return JsonResponse({"Success": False})


class TweetView(generic.CreateView):
    model = Tweet
    fields = ['text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TweetView, self).form_valid(form)
