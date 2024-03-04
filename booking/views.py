from django.shortcuts import render
from EasyStay.models import hotel


# Create your views here.
def index(request):
    return render(request, 'booking/index.html')


def search_rst(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        print('location:',location)
        rsts = hotel.objects.filter(location__icontains=location).all()
        return render(request, 'booking/search_rst.html', locals())
