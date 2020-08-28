import pandas as pd
from uszipcode import SearchEngine
import csv
import os.path

"""
Keep adding these objects for any new infographic you build.
They will all be similar, so utilities for data (ie pandas)
may be brought out and used. In the 'views.py', ensure that 
any new function you build (either for making 'new' pages OR if
you override the existing pages) use these objects and keep this
modular. This is a starting point and can be further improved! And
this can also always be pushed up to the database.
NOTE - half of this class was used to make new datasets/parse
data from a mask dataset/data clean (convering from COUNTY-MASK PREFERENCE
to STATE-MASK PREFERENCE, then comparing that data to STATE-
NEGATIVEPREFERENCE-CASES/MORTALITY/COMBINED)
"""
class MaskInfographic(object):

    us_state_abbrev = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Northern Mariana Islands':'MP',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virgin Islands': 'VI',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'
    }


    def __init__(self, name):
        """This is just naming the object used, nothing else, can make static but
        naming is fun - the states are used to gather all the counties to their states"""
        
        self.name = name
        self.states={}

    def figure_out_state_desires(self, override = False):
        """This only needs to run once (or on local change/data parsing) to convert the county data to a state aggregated dataset
        Leaving in this and not a script in case it needs to be rerun ever again/for example for other
        zipcode based cacluations which are common"""
        
        if(os.path.isfile('../../datasets/maskdata/mask_use_by_state.csv') and override == False):
            return 
        search = SearchEngine(simple_zipcode=False)
        data = pd.read_csv("../../datasets/maskdata/mask-use-by-county.csv", dtype=str)
        columns = data.columns.tolist()
        for i, dat in data.iterrows():
            try:
                #print(dat[columns[0]])
                state_of_code = search.by_zipcode(dat[columns[0]]).state_abbr
                #print(state_of_code)
                never_val = float(dat[columns[1]])
                rare_val = float(dat[columns[2]])
                sometimes = float(dat[columns[3]])
                freq = float(dat[columns[4]])
                always = float(dat[columns[5]])
                new_values = [never_val, rare_val, sometimes, freq, always]
                if state_of_code in self.states:
                    existing_state = self.states[state_of_code]
                    existing_state["ct"] = existing_state["ct"] + 1 #new value afterwards
                    for idx in range(1, len(columns)):
                        self.reaverage_dict(existing_state, columns[idx], new_values[idx-1]) #idx-1 since new_values and columns off by 1
                else:
                    innerValues = {columns[1]:never_val, columns[2]:rare_val, columns[3]:sometimes, columns[4]:freq, columns[5]:always, "ct":1}
                    self.states[state_of_code] = innerValues #a state will start to be averaged.
            except Exception as e:
                print("Exception is " + str(e))
                continue  #just ignore that point - can switch to better source later (better zip code package)
        self.calculate_averages(columns)
        fields = ['state', 'NEVER','RARELY','SOMETIMES','FREQUENTLY','ALWAYS','NEGATIVE']
        self.write_to_csv('../../datasets/maskdata/mask_use_by_state.csv', fields, self.states)

    def calculate_averages(self, columns):
        """This aggregates all the 'negative' actions (ie not really wanting to wear masks) and also
        reaverages the 'values' across the entire state across all counties measured"""
        
        for k, v in self.states.items():
            negative_val = 0
            for i in range(1,len(columns)):
                current_val = v[columns[i]]
                v[columns[i]] = current_val/v["ct"] #correct value
                if i<=3:
                    negative_val += v[columns[i]]
                
            v["NEGATIVE"] = negative_val
            print(v)

    def write_to_csv(self, filename, fields, valuedict):
        """Without using a dataframe - dict should be in a h1, h2, h3, h4 form with key as h1, and h2,h3,h4 in a dict as values, limited by
        the length of the fields - this will allow any length csv to be written assuming followed"""
        
        with open(filename, 'w', newline='') as file:
            fieldnames = fields
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for key, innervalues in valuedict.items():
                write_dict = self.make_write_dict(fields, key, innervalues)
                writer.writerow(write_dict)
    
    def make_write_dict(self, fields, k, innerVs):
        """Creates a 'row' of a CSV file given a dict format of
        {value0:{fields[1]:value1, fields[2]:value2, ....}} which will become
        a csv of : fields[0], fields[1], fields[2], ... (etc...)
        then the : value0 (the key), value1, value2, ... (etc...)
        This 'second' row (the csv row under those csv headers) will
        be what is injected into the dictionary"""

        write_dict = {}
        write_dict[fields[0]] = k
        for idx in range(1, len(fields)):
            write_dict[fields[idx]] = innerVs[fields[idx]]
        return write_dict
    
    def reaverage_dict(self, state_dict, col, new_val):
        """Relying on references changing properly, adds
        to the old value, the new value, for when aggregating
        multiple counties within a state"""
        
        state_dict[col] = (state_dict[col] + new_val)

    def generate_no_mask_to_cases(self):
        """Creates the no masks preferred to cases csv file"""
        
        data_masks = pd.read_csv("../../datasets/maskdata/mask_use_by_state.csv", dtype=str)
        data_state_cases = pd.read_csv("../../datasets/maskdata/recent_states.csv", dtype=str)
        data_state_tested = pd.read_csv("../../datasets/maskdata/testingdata.csv", dtype=str)
        
        states_mask_cases = {}
        for idx, state_nfo in data_state_cases.iterrows():
            state_abbr = self.us_state_abbrev[state_nfo["state"]]
            try:
                row = data_masks.loc[data_masks['state'] == state_abbr]
                total_tested_row = data_state_tested.loc[data_state_tested['State'] == state_nfo["state"]] #for the same state
                total_tested_val = total_tested_row.get("# Tests Performed").tolist()[0] #proportions are used
                states_mask_cases[state_abbr] = {'NEGATIVE': row.get('NEGATIVE').tolist()[0], 
                'cases_prop': float(state_nfo['cases'])/float(total_tested_val)} #note mortality is the same but with 'deaths'
            except Exception as e:
                print("This state does not exist in the mask dataset (due to the weaker python zipcode library - moidfy later) " + str(e))
                continue
        #our dict is states_mask_cases - key is 'state_abbr' and values are the rest of the headers in a dict ('NEGATIVE', 'cases') w/ proper vals
        fields = ['state', 'NEGATIVE', 'cases_prop'] #the fields of the new csv file TODO ensure ratio to cases measured/state population
        url = '../../datasets/maskdata/no_masks_to_cases.csv'
        self.write_to_csv(url, fields, states_mask_cases) #modular fn

    """ ------------------------------------------ DATA PARSING and LOCAL WORK above ----------------------------------------"""
    """ ------------------------------------------Chart Creation Below for Django Site --------------------------------------"""

    def create_graph_one(self, url = 'datasets/maskdata/no_masks_to_cases.csv'):
        """This will generate the first graph, which will use the datasets that the above code computed, 
        which will show, for various states, the number of 'poor decisions' made, and the number of 'cases'."""

        data = pd.read_csv(url) #change url if calling from non django source
        #prefer in the database
        categories = [] #these are the various x-axis values (should be proportions)
        case_numbers = []

        for idx, row in data.iterrows():
            categories.append((float(row['NEGATIVE']),row['state']))
            case_numbers.append(float(row['cases_prop']))

        categories = [str(x[0])[:5] + " " + x[1] for x in sorted(categories, key=lambda x : x[0], reverse=True)] #x axis
        case_numbers.reverse() #to align 

        case_nums = {    #json version of series (y axis) and bar chart name
            'name' : 'Bad masks and State',
            'data' : case_numbers,
            'color' : 'blue'
        }    

        chart = {
            "chart" : {"type" : "column"},
            "title" : {"text" : "Negative Mask Proportions to Case Proportions of Tested in US States"},
            "xAxis" : {"categories" : categories},
            "tooltip": {
                "headerFormat": '<span style="font-size:10px">{point.key}</span><table>',
                "pointFormat": '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
                "footerFormat": '</table>',
                "shared": True,
                "useHTML": True
            },
            "series" : [case_nums]
        }

        #print(chart)

        return chart


    def create_graph_two(self):
        """This will generate the second graph, which will use the datasets from above with mortality rate, showing
        the number of deaths that come from the poor decisions"""
        #TODO MODIFY with new graphs
        data = pd.read_csv('datasets/maskdata/no_masks_to_cases.csv') #change url if calling from non django source
        #prefer in the database
        categories = [] #these are the various x-axis values (should be proportions)
        case_numbers = []

        for idx, row in data.iterrows():
            categories.append((float(row['NEGATIVE']),row['state']))
            case_numbers.append(float(row['cases_prop']))

        categories = [str(x[0])[:5] + " " + x[1] for x in sorted(categories, key=lambda x : x[0])] #x axis

        case_nums = {    #json version of series (y axis) and bar chart name
            'name' : 'Bad masks and State',
            'data' : case_numbers,
            'color' : 'blue'
        }    

        chart = {
            "chart" : {"type" : "column"},
            "title" : {"text" : "Negative Mask Proportions to Case Proportions of Tested in US States"},
            "xAxis" : {"categories" : categories},
            "series" : [case_nums]
        }

        #print(chart)

        return chart

    def create_graph_three(self):
        """This is the third graph that will use the data parsing above to generate a JS ready datastructure
        for this third example"""

        #TODO MODIFY with new graphs!
        data = pd.read_csv('datasets/maskdata/no_masks_to_cases.csv') #change url if calling from non django source (else settings.py root used)
        #prefer in the database
        categories = [] #these are the various x-axis values (should be proportions)
        case_numbers = []

        for idx, row in data.iterrows():
            categories.append((float(row['NEGATIVE']),row['state']))
            case_numbers.append(float(row['cases_prop']))

        categories = [str(x[0])[:5] + " " + x[1] for x in sorted(categories, key=lambda x : x[0])] #x axis

        case_nums = {    #json version of series (y axis) and bar chart name
            'name' : 'Bad masks and State',
            'data' : case_numbers,
            'color' : 'blue'
        }    

        chart = {
            "chart" : {"type" : "column"},
            "title" : {"text" : "Negative Mask Proportions to Case Proportions of Tested in US States"},
            "xAxis" : {"categories" : categories},
            "series" : [case_nums]
        }

        #print(chart)

        return chart

    #feel free to keep adding (but then you'd have to modify the html template to add more + modify the csv headers and the backend by rerunning
    #the backend script + ensure the views/urls all match up to the new number of graphs
    #these are all small changes but that's how to extend more than 3 to 4 graphs. Can follow these 
    #models though, and it should be simple to do as these already showcase how to)

if __name__ == "__main__":
    #If you want to modify the datasets/do extra data-cleaning/processing, please run your code below (also useful for debugging)
    mask_data = MaskInfographic("Testing")
    mask_data.figure_out_state_desires(True) #override to make new csv
    mask_data.generate_no_mask_to_cases() #always overrides automatically
    mask_data.create_graph_one('../../datasets/maskdata/no_masks_to_cases.csv') #testing 
    
    
    



    