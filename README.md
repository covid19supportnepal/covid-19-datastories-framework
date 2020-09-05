# To Run
Follow the quick guide (just the installation part - get django, and the tools needed via pip mentioned below). ENSURE to make this 
root file have a venv in it! 

Go to the directory with manage.py
Use 'python manage.py makemigrations'
Then 'python manage.py migrate' (if you played with code and changed anything/added things via my scripts)
Finally 'python manage.py runserver' (note, only the third needs to be run for small changes in html/css/js, python chanes require the above 2)

And your server should be live and this dynamically generated datastory should play at **localhost::port (usually 8000)/infographic**

**Note - this should be hosted on somewhere that allows django hosting (there are free options for this online).**

# Quick Guide

This was all built in a quick, modular way due to limitations of time since I'm moving back to College this weekend. The purpose of this Django application is to:
- 'Ad-lib' text used in data stories (modularly add in text to any data story of any length with tiny changes)
    - Use Python to take advantage of the full data analytics capabilities of it (since that's where we wanted data analysis, though JS is another option,
    python is better for most people)
    - Use Django's backend to have a powerful way to modularily serve graphs to the front end from backend analysis
    - Run non live scripts to do local backend data cleaning/parsing as needed.
Ensure to have:
    - Django installed, in a virtual environment (python -m venv data_stories)
        - Run this via ./Scripts/activate to open the virtual environment
        - Then install Django (pip install Django)
    - Ensure to have various pip tools installed.
        - django-extensions - **required for backend local scripting and database injections locally**
        - pandas + data analysis friends (numpy, scipy, etc.. - they all install with pip install pandas)
        - uszipcode (pyzipcode too) - these are not optimal but no better ones exist - required for the current 'mask' data story, at least for backend analysis (local analysis)
        - djangify - if you want to convert a future HTML page to a 'django' ready one (ie a NON django page - but you shouldn't and can just use the one I've made probably, and copy it, and edit it for the future - however should one want to convert a future one, this is needed)
    - Ensure to learn how Django works:
        - Templates = Pages served
        - Static = Served Pages static assets (including JS, CSS)
    Quick Filestructure Guide:
    Main Root = Venv file for python virtual space
        - data_stories_project = Main Django project root
            - manage.py = main django code entry point (python manage.py makemigrations, then python manage.py migrate, then python manage.py runserver
            are the three main commands to start the service for the first time/after every change assuming the above is installed)
            - db.sqlite3 = default database that we use to hold 'data-story' items (stories)
                - These are fed into via a Script found in 'scripts' in the DJANGO root (NOT in the VENV root), and use the 'models.py' found in our main app (data_stories_main)
                - So if you want to make a NEW datastory, please add to the CSV file in data_stories_main/data_for_db/data_stories.csv, then run this script using python manage.py runscript (nameofscript without ending - in this case it's 'write_db' (don't use quotes in terminal))
                - This is how to inject the new data into the database so that you can make new datastories.
            - datasets -> This is a file I made personally to hold datasets that we will use for data analysis since this is a data/infographic story generating app. Feel free to organize this as you like - the code currently uses these files in this order, so you will have to change URL locations in code in locations like 'mask_data.py' or 'views.py' or wherever the CSVs are used - feel free to migrate this to the Database as well (so your database contains the data injected via Script from the CSV)
            - data_stories_project -> This is the PROJECT file (NOT the APP file) -> in here are the overall URLs and overall Settings for the whole project which will dictate what backend url is hit - please modify this accordingly, especially when making a new 'app'. For now, though, this should be fine, and does not need to be changed as we only have one app (the 'data story' creating app)
            - data_stories_main -> This is the MAIN APP project! This is the 'modular data story' creator.
                - Within this, the backend URLS, offset from the default urls set in the project root above, connect to the view controller and then to the actaul html/css files.
                - Here, to add/change an infographic:
                    - Make a new HTML file (nearly identical copy of the existing ones) OR just use the existing one BUT modify the 'data' it pulls.
                    - Ensure the data you want is IN the database via the injection above.
                    - Ensure the otherdata for the 'data analysis' is read and properly converts things to the Python-JS HighCharts form (see mask_data.py as the example).
                        - You would essentially make another class like mask_data.py but for whatever else you were analyzing. This means that you may
                        want to organize it better than I did (I did this quickly since I have to move back to College this weekend) for future data
                        stories, but feel free to use the one I made for masks as a reference. Improving means separating out classes that analyze data, with classes that Django uses to 'pull' data once finalized (of course, you may modify this as well and use Django's database instead of CSVs for that final reading - this is all up to you, future volunteer/engineer).
                    - Check for consistency across urls.py, the index.html urls (the ones that point to the function in views.py that generates the page AND the one that generates the graph MUSt have the same name), and the views.py! And ensure the models.py has the proper model you want in your database (esp if you make a new model for a 'longer' data story, you can just ensure this handles it - each class here will be a 'table' in the database, a sql database). You can use cmd tools or Heidi SQL or similar for the database to read it/see it, and you can always create code to do the same in Python.
                    - Ensure consistency in apps.py and the apps in the settings.py and in the project root - this is already done for this app, but this is for future apps if built.
                    - The 'data_reading' directory is where each new 'data story' parsing and chart creation to post modularily on the website goes!

# To add a new Data Story (New HTML page)
Let's start by making a new HTML page - copy the one in 'templates/infographic' and call it whatever you want ('index2.html' or even better, in the future, maybe a 'vaccine_data.html'). Now, let's make a story that has '8 paragrahs' and '2' graphs - the default in that copied one is '4' paragraphs (intro, middle, end, extra) and '3' graphs. Remember, you can always change this - to add more graphs, in your html file, ensure to have more modules of this, and name it appropriately. (ie container1, 2, 3, etc...
and of course function_one, function_two (here, the function is named chart_one - THIS MUST match urls.py AND view.py))).
So this below is a 'chart' module - let's say you have 2 charts - you have 2 of these and ensure to name them properly (assmuming these are the only things named container1 through 2, it should be okay, else give them unique ids!). You can have as MANY or as FEW graphs as you want, assuming that your view.py and urls.py match! Note - these 'modules' go in random places in your HTML code, up to your decision where to display them!

```
....code above

- <div style = "resize:both;" id="container1" data-url="{% url 'data_stories_main:info2_one' %}"></div> <!-- this invokes a view -->
            <script>
              $.ajax({
                url: $("#container1").attr("data-url"), //connects to the attr in the div above
                dataType: 'json',
                success: function (data) {
                  Highcharts.chart("container1", data);
                }
              });
            </script>

.... code in between

- <div style = "resize:both;" id="container2" data-url="{% url 'data_stories_main:info2_one' %}"></div> <!-- this invokes a view -->
            <script>
              $.ajax({
                url: $("#container2").attr("data-url"), //connects to the attr in the div above
                dataType: 'json',
                success: function (data) {
                  Highcharts.chart("container2", data);
                }
              });
            </script>

.... code below
```

What about the '8' paragraphs? Well by default, the 'models.py' database model schema we have has 4 paragraphs that it stores in the database, and that we inject via the script as mentioned above in the 'Quick Guide'. To have a new 'model' with 8 paragraphs, either modify the existing one or make a new 'model', then use the scripts to inject into it (so the scrip found in write_db.py in the djagnoroot/scripts folder) with the new changes. 4 is likely a good starting point and will be modular, but changing this is a 5 to 10 minute chage, hence that is also modular for future data stories.

```
class DataStories(models.Model):
    infographicName = models.TextField()
    infographicIntro = models.TextField()
    infographicMiddle = models.TextField()
    infographicEnd = models.TextField()
    infographicExtra = models.TextField(blank=True)
    #feel free to modify this 'schema' object or make a new one
    #infographicPar5 = models.TextField()
    #infographicPar6 = models.TextField()
    #infographicPar7 = models.TextField()
    #infographicPar8 = models.TextField()
    #These would be the changes to get a '8' element datatable, and then you can inject via the Script with 8 paragraphs (or leave some blank if you #wanted) via the 'data_for_db/data_sotires.csv', injected (and overriden/etc... for changes) by the script in the project root
```
Now, just ensure that you've either overridden the existing 'urls.py' with the new view.py functions, or you've made new view.py functions (note that you can have many many view modules, it can be in it's own view directory) - let's assume you've made new ones (ie this is a 'new' page that is at hostname:infographic2/ instead of hostname:infographic/ (so the latter goes to the Mask one we made, and the former to the new one). Note the NAME below (Vaccine Blues!) is the same name used in the database injected via the csv (in this test/fake example).

```
path('infographic2/', views.infographic_two, {"info_display":"Vaccine Blues!"},name='infographic_two'), #feel free to modify this OR add new ones
path('infographic2/data', views.info2_one, name='info2_one'),
path('infographic2/data2', views.info2_two, name='info2_two'),
```
These MUSt match the name used in the HTML above in the 'url' sections AND must exist in the 'views.py', which is where the magic happens (where the backend data is collected via these modules). Note all of these above can just be 'replaced' in the existing data story by overriding it with 'new' database entries and new 'dataset' entires - that would take 5 minutes to do (assuming same size data story and 3 charts). This example is for the most unique use case (all new, different length data stories and different amount of charts).

```
def infographic_two(request, info_display):
    """The purpose of this function is to generate and return the data story infographic.
    Note that adding in future infographics is as simple as making a new function like this and 
    adding it to the 'urls.py' in this app (data_stories_main) as a new endpoint.

    request: a generic HTTP (S) GET request that hits one of the urls defined in urls.py (main) + urls.py (app)
    returns a rendered page that contains the results of our backend data analysis
    """
    dataModel, headers, data = Config.retrieve_data(info_display)
    #note here, we generate the graph from data and pass to D3.js/some chart JS module OR django chart module and load/render below
    return render(request, 'infographic/vaccine_data.html', {"datastory":dataModel, "headers":headers})

def info2_one(request):
    """This will generate the charts for a particular dataset that you decide based on your use case.
    This is used currently for the mask, but feel free to add on more functions."""
    mask_chart_data_creator = MaskInfographic("chart_one")
    return JsonResponse(mask_chart_data_creator.create_graph_one())

def info2_two(request):
    """This will generate the second set of charts for the infographic fn"""
    mask_chart_data_creator = MaskInfographic("chart_two")
    return JsonResponse(mask_chart_data_creator.create_graph_two())

```
This MUST be your views.py (or in some modular form of views.py somewhere in a directory of views). The 'Config' is the configuration that I use - feel free to modify it - to reveal the name of the 'database table' entry that we should use for any particular name. So you must ensure that this is spelled properly (in the 'info_display' passed in the urls must be the same as something in the database).

These functions render to that html page so ensure that html page is properly spelled and is ready to accept all this! Ensure that in the html page, your template can receive everything in 'dataModel' and 'headers'.

## Data Analysis

And that's it! This adds a new very different data story, without much changes. Of course, the 'most fun' part on this is to parse the new data, and you can do that in the code you write in the 'data_reading' directory! I have one example, which does local parsing of data, and then creates the javascript ready charts for highchart. Feel free to make your own class/package/whatver to do any parsing, even push to the database, etc... and then use that to power the graphs! This MUST be what is used in the view.py above (or in any organiztion you make it). This will allow for the website to get the JSON as it expects it. If you change HighCharts, modify the HTML javascript module, and also ensure the JsonResponse object created in your data parsing modules and given the functions in the 'views.py' modules are also matching the new chart making tool! I keep all my datasets in the datasets directory in the root of the django folder - again, feel free to modify, but that is for local development and data parsing/cleaning.

### Framework Creation and Support
This framework was created by Arpan Kaphle, who volunteered with covid19supportnepal during the end of summer 2020. I wish future developers the best of luck as we hopefully get out of this pandemic soon, and am appreciative of covid19supportnepal, as well as all of you guys who are helping get information out to people! Feel free to contact me via the email covid19supportnepal has on hand for any future questions. I wrote this over the course of a few hours prior to returning to university, so I know this readme is rushed (and the code, while attempted to be modular to future data stories, may look rushed but hopefully good enough to use!).

