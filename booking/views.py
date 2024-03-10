from django.shortcuts import render
from EasyStay.models import hotel
from django.http import HttpResponse



# Create your views here.
def index(request):
    return render(request, 'booking/index.html')


def search_rst(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        print('location:',location)
        rsts = hotel.objects.filter(city=location).all()
        for rst in rsts:  # get the star of each review and show in star icon
            rst.stars = range(rst.star)
            rst.non_stars = range(5 - rst.star)

        return render(request, 'booking/search_rst.html', locals())
