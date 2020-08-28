from data_stories_main.models import DataStories
import pandas as pd

def read_csv_data(data_url):
    """Reads the badge data from csv
    
    returns: the pandas dataframe of the csv data"""

    data = pd.read_csv("data_stories_main/data_for_db/"+data_url+".csv")

    return data

def push_into_db(data):
    """Takes the data, and injects anything new into our database

    data: a dict object that contains our csv data
    returns: nothing, just populates database
    """

    print(data)
    columns = data.columns.tolist()
    for i, dat in data.iterrows():
        try:
            values = [dat[columns[0]], dat[columns[1]], dat[columns[2]], dat[columns[3]], dat[columns[4]], dat[columns[5]]]
            obj, created = insertData(values) #insert or sees it already exists
            print("VALUES IS " + str(values[5]))
            print("Bool is " + str(created))
            if(created == False and str(values[5])=="1"):
                print("You have updated " + values[0])
                replaceData(dat)
        except:
            print("Error when working with " + i + " and " + dat)
        

def insertData(dat):
    """A textbook way to insert or get existing data in the database

    dat : the data that we are inserting into the database
    returns the new object if it's created or the existing object, and the boolean of wheter or not it was created (True) or 
    it already exists (FALSE)
    """

    print(DataStories.objects.filter(infographicName = dat[0]))
    if DataStories.objects.filter(infographicName = dat[0]): #to ensure it updates when it should (ie if exists, leaves, elif empty, create cautiously)
        return False, False
    print("Made")
    return DataStories.objects.get_or_create(infographicName=dat[0], infographicIntro = dat[1], infographicMiddle = dat[2],
    infographicEnd = dat[3], infographicExtra = dat[4])


def replaceData(dat):
    """This will update a existing row with the specified fields - we hold the first name constant - please delete them via making 
    another script here, or directly from the heidisql - deleting isn't much of a concern (feel free to reference 
    this :https://djangobook.com/mdj2-models/)

    dat : the data we are inserting into the database
    returns nothing, just autoreplaces the data and any return value is ignored
    """

    DataStories.objects.filter(infographicName = dat[0]).update(infographicIntro = dat[1], infographicMiddle = dat[2],
    infographicEnd = dat[3], infographicExtra = dat[4])

"""
For future volunteers - see this to read the database/test any task for reading from the DB
"""
def test_reading_db():
    seeData = DataStories.objects.all()
    print(seeData)
    headers = DataStories._meta.fields
    print(len(headers))
    for i in headers:
        print(i.name)
    for eachData in seeData:
        print(eachData.infographicName)
        print(eachData.infographicMiddle)





def run():
    print("Ensure that your file is in the data_for_db directory")
    #filename = input("Please enter your csv file name with data (without 'csv' at the end): ")
    filename = "data_stories"
    to_inject = read_csv_data(filename)
    push_into_db(to_inject)
    #test_reading_db()
    



"""
While this could be done in 'each' run of the website, automatically in views.py, but I think injection
should be done this way, and only pulling from the database should be done that way - however, feel free
to modify, using this as a base to create that online one - note to this use, use this https://github.com/django-extensions/django-extensions
I've already installed it but see that for more information
'python manage.py runscript write_db.py'
Just run that each time you updated your 'data_for_db' directory, and want to input new data into the database!
Note - the Scripts folder is in the 'django main' (data_stories_project) dir (do NOT confuse w/ the venv Scripts folder at root)
If you want, you can specify 'scripts per app' (so make a Scripts folder in an app, like in 'data_stories_main')! This will use
these first, before using the global one found in the django main folder.
Feel free to extend this to more database operations as needed. 
Feel free to use this to 'test' as well!
"""