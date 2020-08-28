from django.shortcuts import render
import random as rd
from .models import DataStories
from django.http import JsonResponse
from .data_reading.mask_data import MaskInfographic


def index (request): 
    return render(request, 'main/index.html') #uses what's in 'templates' as the 'base'
#so by default this is really /data_stories_project/data_stories_main/templates/
#then it looks for the above link (so ...templates/main/index.html).

def test (request):
    test_choice = int(rd.random()*2+1)
    url_one = 'main/index.html'
    url_two = 'test/index.html'
    if test_choice != 1:
        return render(request, url_two)
    else:
        return render(request, url_one)

def infographic(request, info_display):
    """The purpose of this function is to generate and return the data story infographic.
    Note that adding in future infographics is as simple as making a new function like this and 
    adding it to the 'urls.py' in this app (data_stories_main) as a new endpoint.

    request: a generic HTTP (S) GET request that hits one of the urls defined in urls.py (main) + urls.py (app)
    returns a rendered page that contains the results of our backend data analysis
    """
    dataModel, headers, data = Config.retrieve_data(info_display)
    #note here, we generate the graph from data and pass to D3.js/some chart JS module OR django chart module and load/render below
    return render(request, 'infographic/index.html', {"datastory":dataModel, "headers":headers})

def chart_one(request):
    """This will generate the charts for a particular dataset that you decide based on your use case.
    This is used currently for the mask, but feel free to add on more functions."""
    mask_chart_data_creator = MaskInfographic("chart_one")
    return JsonResponse(mask_chart_data_creator.create_graph_one())

def chart_two(request):
    """This will generate the second set of charts for the infographic fn"""
    mask_chart_data_creator = MaskInfographic("chart_two")
    return JsonResponse(mask_chart_data_creator.create_graph_two())

def chart_three(request):
    """This will generate the second set of charts for the infographic fn"""
    mask_chart_data_creator = MaskInfographic("chart_three")
    return JsonResponse(mask_chart_data_creator.create_graph_three())
    
    


"""
A configuration class you can exchange for future datasets, returns the 
'datamodel info' and the 'dataset url' for the data related to this data story. Note, this assumes 
you want to use the single url (infographic fns url above) for MULTIPLE different stories.
Feel free to make new functions and reuse this as well (this allows either changing the datastory on
one url OR you can use this for multiple datastory fns on different urls (make sure the urls.py and the new
fns are generated above in the view fns!))
"""
class Config(object):

    @staticmethod
    def retrieve_data(info_display):
        if "Mask" in info_display:
            return DataStories.objects.get(infographicName=info_display), DataStories._meta.fields,"../datasets/maskdata" 
            #//TODO give the real data for the graph directly
        
             
        


    