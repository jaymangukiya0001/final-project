from django.shortcuts import render,get_object_or_404,redirect
from .models import Listing
from django.core.paginator import Paginator,EmptyPage
from .choices import price_choices, category_choices, state_choices
from django.contrib.auth.decorators import login_required
from .forms import UpdateForm, ListingForm
# Create your views here.


def listings(request):
    listings = Listing.objects.order_by('-last_date').filter(is_published=True)
    paginator = Paginator(listings, 9)
    page = request.GET.get('page')
    page_listings  = paginator.get_page(page)
    context = {
        'listings': page_listings
    }
    return render(request, 'listings/listings.html', context)

def listing(request,pk):
    listing=get_object_or_404(Listing,pk=pk)
    contex={
        'listing':listing
    }
    return render(request,'listings/listing.html',contex)


def search(request):
    query_set = Listing.objects.order_by('-last_date').filter(is_published=True)
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            print("1")
            query_set = query_set.filter(decription__icontains=keywords)
    if 'city' in request.GET:
        print("city")
        city = request.GET['city']
        if city:
            print("city2")
            query_set = query_set.filter(city__iexact=city)
    if 'category' in request.GET:
        print("category")
        category = request.GET['category']
        if category:
            query_set = query_set.filter(category__iexact=category)
    if 'state' in request.GET:
        print("state")
        state = request.GET['state']
        if state:
            query_set = query_set.filter(state__iexact=state)
    if 'price' in request.GET:
        print("price")
        price = request.GET['price']
        if price:
            query_set = query_set.filter(price__lte=price)
    context = {
        'query_set': query_set,
        'price_choices': price_choices,
        'state_choices': state_choices,
        'category_choices': category_choices,
        'values': request.GET
    }
    return render(request,'listings/search.html',context)


@login_required
def create(request):
    if request.method =='POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.owner = request.user
            new.save()
            return redirect('dashboard')
        else:
            pass
    else:
        return render(request, 'listings/create.html', {'form':ListingForm()})

@login_required
def update(request, pk):
    listing = get_object_or_404(Listing, pk=pk, owner=request.user)
    context = {
        'form': UpdateForm(instance=listing),
        'update': True
    }
    if request.method=="POST":
        pass
    else:
        return render(request, 'listings/create.html', context)

@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, owner=request.user)
    if request.method=="POST":
        listing.delete()
        return redirect('dashboard')



