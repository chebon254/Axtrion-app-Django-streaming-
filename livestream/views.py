from django.shortcuts import render

# Create your views here.
def livestream(request, room_name):
    return render(request, 'livestream/livestream.html', {'room_name': room_name})