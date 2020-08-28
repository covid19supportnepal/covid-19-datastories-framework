from . import views
from django.urls import path

app_name = 'data_stories_main'

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('infographic/', views.infographic, {"info_display":"Your Mask Matters!"},name='infographic'), #feel free to modify this OR add new ones
    path('infographic/data', views.chart_one, name='chart_one'),
    path('infographic/data2', views.chart_two, name='chart_two'),
    path('infographic/data3', views.chart_three, name='chart_three'),
    #example, new story, just add
    #path('new_data_story/', views.new_story_fn, name = 'new_story_fn')
    #and so on - ensure the page is created. However, there are ways to
    #reuse the 'same' url with different data (ie if you place a different
    #dataset of the same 'style' in the given location, mask_story may 
    #be replaced with a new one that has text and everything in csv
    #files - up to you on the implementation but this is modular for future
    #expansion)
]

"""This is in the hostname/(locationOfThisApp)/....
In other words, this thinks the root is (locationOfThisApp) and starts from /
"""

"""
Setting the 'main' code uril path to be from nothing and letting views.index populate it
which it will do via going in to templates (like that comment above says).
Then, we need to make another one, (another 'data_stories') directory on the same
level as 'main' which will contain OVERALL urls, one for the 'admin' site, one for
this site. So in the admin one, it will also have a urls.py that is '' from the 
beginning, but this OVERALL makes that 'beginning' for admin be /admin/etc...
but for us it makes it literally 'hostname/etc...
"""


"""
The 'namespace' is set in the 'app' 'main'.
The admin is set in 'admin.py' AND if we want, we can have our own
separate 'app' for admin!
In other words, we can run a hundred 'different' initial apps under
ONE hostname, and here, we can decide which is the 'starting' point for 
all those hostnames, under the 'data_stories' 'project'! Since all
these different apps will be a part of the same 'project'.
admin = 1 app (hostname/admin/innerUrlsofAdmin)
main = another app (hostname/innerUrlsofMain)
app2 = (hostname/app2url/innerUrlsofApp2)
and so on....
Note - this allows our service to behave as a backend! Because instead of 'pushing
the site', which is what it does as a 'framework' (esentially putting both 
backenda nd frontend into 'one' part of itself together, and kind of serving and powering
itself server side to also have the client work there) BUT if we wanted to
we could eailsy just have this code be 'hit' from outside clients as an API and this
be a purely backend service (of course we can use graphQL if node, but this is python
based, so REST api makes sense, etc...) -> And thus we can build powerful ml model
result tools that others can hit and so on. This is the backend/frontend separation
and here is the 'overall' url creator, and then each 'app' has the inner urls
created, which to it, seem like it's at the 'forefront' (kind of like the http
thing in coral (/churchill vs /default etc...)).
"""
