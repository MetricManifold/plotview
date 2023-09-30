from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Directory, Folder
from .utils import plot_data
from django.views import generic
import os


def directory_list(request):
    directories = Directory.objects.all()
    return render(request, 'plotter/directory_list.html', {'directories': directories})

def folder_list(request, directory_id):
    directory = get_object_or_404(Directory, pk=directory_id)
    
    # Get a list of all folders in the directory on the filesystem
    directory_path = directory.path
    directory_folders = os.listdir(directory_path)
    
    # Get a list of all folders stored in the database for this directory
    db_folders = Folder.objects.filter(directory=directory)
    
    # Create a set of folder names for quick comparison
    directory_folder_names = set(directory_folders)
    db_folder_names = set(folder.name for folder in db_folders)
    
    # Find new folders in the directory and add them to the database
    new_folders = directory_folder_names - db_folder_names
    for folder_name in new_folders:
        Folder.objects.create(directory=directory, name=folder_name)
    
    # Find folders in the database that no longer exist in the directory and delete them
    deleted_folders = db_folder_names - directory_folder_names
    Folder.objects.filter(directory=directory, name__in=deleted_folders).delete()
    
    # Get the updated list of folders for this directory
    folders = Folder.objects.filter(directory=directory).order_by('-name')
    
    return render(request, 'plotter/folder_list.html', {'directory': directory, 'folders': folders})


def generate_picture_view(request, folder_id):
    folder = get_object_or_404(Folder, pk=folder_id)
    plot_data(folder)
    return redirect('folder_list', directory_id=folder.directory.pk)


class IndexView(generic.ListView):
    template_name = "plotter/index.html"
    context_object_name = "directories"
    
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Directory.objects.order_by("-path")


