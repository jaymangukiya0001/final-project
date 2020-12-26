from django.shortcuts import render
from django.contrib.humanize.templatetags.humanize import intcomma
from listings.models import Listing
from listings.choices import price_choices, category_choices, state_choices
# Create your views here.
def index(request):
    listings = Listing.objects.order_by('-last_date').filter(is_published=True)[:3]
    context = {
        'listings': listings,
        'price_choices': price_choices,
        'state_choices': state_choices,
        'category_choices': category_choices,
    }
    return render(request, 'pages/index.html', context)
 

def about(request):
    return render(request,"pages/about.html")