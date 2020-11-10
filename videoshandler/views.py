from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import wall, Videos
from django.contrib.auth import authenticate, login
from .forms import VideosForm, SearchForm


# Create your views here.
def index(request):
    return render(request, 'videoshandler/index.html')


def dashboard(request):
    return render(request, 'videoshandler/dashboard.html')


def add_video(request, pk):
    form = VideosForm()
    sform = SearchForm()

    context = {
        'form': form,
        'sform': sform

    }
    if request.method == 'POST':
        filled_form = VideosForm(request.POST)
        if filled_form.is_valid():
            video = Videos()
            video.wall = wall.objects.filter(pk=pk).first()
            video.title = filled_form.cleaned_data['title']
            video.url = filled_form.cleaned_data['url']
            video.youtube = filled_form.cleaned_data['youtube']
            video.save()
            return redirect('dashboard')

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
