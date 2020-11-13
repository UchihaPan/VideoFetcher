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

# YOUTUBEAPIKEY = 'AIzaSyDbr2kBRaRbnGwUw49pcmA7g2O_8UOjUW4'
# YOUTUBEAPIKEY = 'AIzaSyAhNdnruZNxgWsqVNeecrLTzQZz4IQUYYQ'
YOUTUBEAPIKEY = 'AIzaSyD9zBjS0uWDQ5u9QvN0rTaWCb6H6l45e3Y'


def index(request):
    return render(request, 'videoshandler/index.html')


def dashboard(request):
    return render(request, 'videoshandler/dashboard.html')


def search(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        encoded_search_term = urllib.parse.quote(search_form.cleaned_data['search'])
        response = requests.get(
            f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={encoded_search_term}&key={YOUTUBEAPIKEY}')
        return JsonResponse(response.json())
    return JsonResponse(
        {'error': 'Something is Wrong'}
    )


def add_video(request, pk):
    form = VideosForm()
    sform = SearchForm()

    wallm = wall.objects.get(pk=pk)
    if request.user != wallm.user:
        raise Http404

    if request.method == 'POST':
        filled_form = VideosForm(request.POST or None)
        if filled_form.is_valid():
            video = Videos()
            video.wall = wallm
            video.url = filled_form.cleaned_data['url']
            parsed_url = urllib.parse.urlparse(video.url)
            video_id = urllib.parse.parse_qs(parsed_url.query).get('v')
            if video_id:

                video.youtube = video_id[0]
                response = requests.get(
                    f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={video_id[0]}&key={YOUTUBEAPIKEY}')
                json = response.json()
                title = json['items'][0]['snippet']['title']
                print(title)
                video.title = title

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


class Createwall(generic.CreateView):
    model = wall
    fields = ['title']
    template_name = 'videoshandler/createwall.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(Createwall, self).form_valid(form)
        return redirect('dashboard')


class Updatewall(generic.UpdateView):
    model = wall
    fields = ['title']
    template_name = 'videoshandler/updatewall.html'
    success_url = reverse_lazy('dashboard')


class Detailwall(generic.DetailView):
    model = wall
    template_name = 'videoshandler/detailwall.html'


class Deletewall(generic.DeleteView):
    model = wall
    template_name = 'videoshandler/deletewall.html'
    success_url = reverse_lazy('dashboard')
