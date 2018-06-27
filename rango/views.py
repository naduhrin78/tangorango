from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
# from django.template import RequestContext
# from django.shortcuts import render_to_response
# from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from rango.models import Category, Page, UserProfile
from rango.forms import CatForm, PageForm, UserProfileForm
from django.template.defaultfilters import slugify
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User
from registration.backends.simple.views import RegistrationView
from rango.search import run_query

def get_category_list(max = 0, starts_with =''):
    cat_list = []

    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)

    return cat_list[:max]

def suggest_category(request):
    cat_list = []
    starts_with = ''

    if request.method == 'GET':
        starts_with = request.GET['suggestion']

    cat_list = get_category_list(8, starts_with)

    context_dict = {'cats':cat_list}

    return render(request, 'rango/category_list.html',  context_dict)


@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0

    if cat_id:
        category = Category.objects.get(id=int(cat_id))
        category.likes = category.likes+1
        likes = category.likes
        category.save()

    return HttpResponse(likes)


@login_required
def dislike_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0

    if cat_id:
        category = Category.objects.get(id=int(cat_id))
        category.likes = category.likes-1
        likes = category.likes
        category.save()

    return HttpResponse(likes)


def list_profiles(request):
    userprofile_list = UserProfile.objects.all()
    context_dict = {'userprofile_list': userprofile_list}
    return render(request,'rango/list_profiles.html', context_dict)

def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        HttpResponseRedirect(reverse('index'))

    userprofile = UserProfile.objects.get(user=user)

    form = UserProfileForm({'website': userprofile.website, 'picture': userprofile.picture})

    if request.method == 'POST':
        form = UserProfile(request.POST, request.FILES, instance = userprofile)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('profile', user.username)
        else:
            print(form.errors)

    context_dict = {'userprofile': userprofile, 'selecteduser': user, 'form': form}

    return render(request, 'rango/profile.html', context_dict)


def search(request):
    result_list=[]
    if request.method == 'POST':
        query = request.POST['query'].strip()
    if query:
        result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})

def track_url(request):

    context_dict = {}

    if request.method == 'GET':
        if 'slug' in request.GET:
            try:
                page = Page.objects.get(slug=request.GET['slug'])
                page.views = page.views + 1
                page.save()
                return HttpResponseRedirect(page.url)

            except Page.DoesNotExist:
                return render(request, 'rango/index.html', context_dict)

    else:
        render(request, 'rango/category.html', context_dict)


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user=None):
        return '/rango/'

def get_server_side_cookies(request, cookie, default = None):
    val = request.session.get(cookie)
    if not val:
        val = default
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookies(request, 'visits', '1'))
    last_visit = get_server_side_cookies(request,'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit[:-7],"%Y-%m-%d %H:%M:%S")

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits+1
        request.session['last_visit'] = str(datetime.now())

    else:
        request.session['last_visit'] = last_visit

    request.session['visits'] = visits


# Used for custom logout view
"""
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('index'))
"""

# Used for custom logout view
"""
def login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password= password)

        if user:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse('Your rango account is disabled.')

        else:
            return HttpResponse('Invalid login details.')

    else:
        return render(request, 'rango/login.html', {})
"""

# Used for custom register view
def register_profile(request):

    userproform = UserProfileForm()

    if request.method == 'POST':
        userproform = UserProfileForm(data=request.POST)

        user = request.user

        if userproform.is_valid():

            userpro = userproform.save(commit=False)

            userpro.user = user

            if 'picture' in request.FILES:
                userpro.picture = request.FILES['picture']

            userpro.save()

            return HttpResponseRedirect(reverse('index'))

        else:
            print(userproform.errors)

    context_dict = {'profile_form': userproform}

    return render(request, 'rango/register.html', context_dict)


@login_required
def add_cat(request):

    form = CatForm()

    if request.method == 'POST':
        form = CatForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)

        else:
            print(form.errors)

    context_dict = {'form': form}

    return render(request, 'rango/add_category.html', context_dict)


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug = category_name_slug)

    except Category.DoesNotExist:
        category = None

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            page.views = 0
            page.category = category
            page.save()
            return show_cat(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'category':category, 'form':form}

    return render(request, 'rango/add_page.html', context_dict)

def show_cat(request, category_name_slug):

    category = None
    pages = None
    try:
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category)

    except Category.DoesNotExist:
        return search(request)

    context_dict = {'category':category, 'pages':pages}

    return render(request, 'rango/category.html', context_dict)

def mod_cat(request):
    category_name_slug = None

    if request.method == 'POST':
        category_name_slug = slugify(request.POST['query'])

    return show_cat(request, category_name_slug)




def sanitize_categories():

    cat_list = list(Category.objects.order_by('-likes'))
    page_list = list(Page.objects.order_by('-views'))

    out_cat = []

    for cat in cat_list:
        name = cat.name
        found = False
        for page in page_list:
            if page.category.name == name:
                found = True
                break

        if found is True:
            out_cat.append(cat)

    return out_cat, page_list



def index(request):
    # remove categories with no pages

    cat_list, page_list = sanitize_categories()

    # pool top 5

    # cat_list = Category.objects.order_by('-likes')[:5]

    cat_list = cat_list[:5]

    # page_list = Page.objects.order_by('-views')[:5]

    page_list = page_list[:5]

    context_dict = {'categories': cat_list, 'pages': page_list}

    visitor_cookie_handler(request)

    context_dict['visits'] = request.session['visits']

    return render(request, 'rango/index.html', context_dict)


def about_page(request):

    context_dict ={'change_this': 'molo!'}

    return render(request, 'rango/about.html', context_dict)
