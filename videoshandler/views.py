from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import wall, Videos
from django.contrib.auth import authenticate, login
from .forms import VideosForm, SearchForm
import urllib
import requests
from django.http import Http404, JsonResponse
from django.forms.utils import ErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import random


# YOUTUBEAPIKEY = 'AIzaSyAhNdnruZNxgWsqVNeecrLTzQZz4IQUYYQ'
# YOUTUBEAPIKEY = 'AIzaSyD9zBjS0uWDQ5u9QvN0rTaWCb6H6l45e3Y'
# YOUTUBEAPIKEY = 'AIzaSyDp_RN6UCYMeyRs_QS-NuIdsu4lkcmgSRc'
def randomyoutube():
    youtube = ['AIzaSyDbr2kBRaRbnGwUw49pcmA7g2O_8UOjUW4', 'AIzaSyAhNdnruZNxgWsqVNeecrLTzQZz4IQUYYQ','AIzaSyD9zBjS0uWDQ5u9QvN0rTaWCb6H6l45e3Y', 'AIzaSyDp_RN6UCYMeyRs_QS-NuIdsu4lkcmgSRc','AIzaSyBlsAznmEevlzTvuRoBURCyUC8axgraS-g']
    n = random.randint(0, 4)
    return youtube[n]


YOUTUBEAPIKEY = randomyoutube()
print(YOUTUBEAPIKEY)


def index(request):
    recent = wall.objects.all().order_by('-id')[:3]

    context = {
        'recent': recent
    }
    return render(request, 'videoshandler/index.html', context)


@login_required
def dashboard(request):
    users_hall = wall.objects.filter(user=request.user)
    context = {
        'users_hall': users_hall
    }
    return render(request, 'videoshandler/dashboard.html', context)


@login_required
def search(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        search_term = urllib.parse.quote(search_form.cleaned_data['search'])
        response = requests.get(
            f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={search_term}&key={YOUTUBEAPIKEY}')
        return JsonResponse(response.json())
    return JsonResponse(
        {'error': 'Something is Wrong'}
    )


@login_required
def add_video(request, pk):
    form = VideosForm()
    sform = SearchForm()

    wallm = wall.objects.get(pk=pk)
    if request.user != wallm.user:
        raise Http404

    if request.method == 'POST':
        form = VideosForm(request.POST or None)
        if form.is_valid():
            video = Videos()
            video.wall = wallm
            video.url = form.cleaned_data['url']
            parsed_url = urllib.parse.urlparse(video.url)
            video_id = urllib.parse.parse_qs(parsed_url.query).get('v')
            if video_id:

                video.youtube = video_id[0]
                response = requests.get(
                    f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={video_id[0]}&key={YOUTUBEAPIKEY}')
                json = response.json()
                title1 = json['items'][0]['snippet']['title']
                video.title = title1

                video.save()
                return redirect('detail', pk)

            else:
                errors = form.errors.setdefault('url', ErrorList())
                errors.append('please enter correct url')

    context = {
        'form': form,
        'sform': sform,
        'wallm': wallm

    }
    return render(request, 'videoshandler/add_video.html', context=context)


class Signup(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'videoshandler/register.html'

    def form_valid(self, form):
        view = super(Signup, self).form_valid(form)
        username, password = form.cleaned_data['username'], form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


class Createwall(LoginRequiredMixin, generic.CreateView):
    model = wall
    fields = ['title']
    template_name = 'videoshandler/createwall.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(Createwall, self).form_valid(form)
        return redirect('dashboard')


class Updatewall(LoginRequiredMixin, generic.UpdateView):
    model = wall
    fields = ['title']
    template_name = 'videoshandler/updatewall.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        video = super(Updatewall, self).get_object()
        if not video.user == self.request.user:
            raise Http404
        return video


class Detailwall(generic.DetailView):
    model = wall
    template_name = 'videoshandler/detailwall.html'


class Deletewall(LoginRequiredMixin, generic.DeleteView):
    model = wall
    template_name = 'videoshandler/deletewall.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        deleteview = super(Deletewall, self).get_object()
        if not deleteview.user == self.request.user:
            raise Http404
        return deleteview


class Deletevideo(LoginRequiredMixin, generic.DeleteView):
    model = Videos
    template_name = 'videoshandler/deletevideo.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        deletevideo = super(Deletevideo, self).get_object()
        if not deletevideo.wall.user == self.request.user:
            raise Http404
        return deletevideo
