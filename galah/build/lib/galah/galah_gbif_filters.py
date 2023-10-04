import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_table_from_html(url,chosen_title,column_titles):

    # get parameters from website
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')

    # find the title of table and get title
    table_titles = soup.find_all('h3')
    for i,title in enumerate(table_titles):
        if title.text == chosen_title:
            index=i
    table_to_parse = soup.find_all('table')[index]

    # parameter dataframe - can this be gotten automatically?
    df = pd.DataFrame(columns=column_titles)

    if chosen_title == "Query parameters explained":
        data = table_to_parse.tbody.find_all('tr')
    elif chosen_title == "Enum Constant Summary":
        data = table_to_parse.find_all('tr')
    else:
        raise ValueError("{} is not what we are checking for.".format(chosen_title))

    # get data for all parameters
    for row in data:  

        # Find all data for each column
        columns = row.find_all('td')
        
        # if columns aren't empty, get data within columns
        if(columns != []):

            temp_dict = {}

            # check for fields or assertions
            if chosen_title == "Query parameters explained":

                # get parameter and description
                for i in range(len(column_titles)):
                    temp_dict[column_titles[i]] = columns[i].text.strip()

            elif chosen_title == "Enum Constant Summary":

                raw_data = columns[0].text.strip().split("\n")
                for i in range(len(column_titles)):
                    temp_dict[column_titles[i]] = raw_data[i]

            else:

                raise ValueError("{} is not what we are checking for.".format(chosen_title))

            # add this to the DataFrame
            tempdf = pd.DataFrame(temp_dict,index=[1])
            df = pd.concat([df,tempdf],ignore_index=True)

    return df

def main():

    # make sure the URLs are here
    gbif_parameters_url = "https://www.gbif.org/developer/occurrence#parameters"
    gbif_assertions_url = "https://gbif.github.io/gbif-api/apidocs/org/gbif/api/vocabulary/OccurrenceIssue.html"

    # get the dataframe
    param_df = get_table_from_html(gbif_parameters_url,"Query parameters explained",["Parameter","Description"])
    assertion_df = get_table_from_html(gbif_assertions_url,"Enum Constant Summary",["ID","Description"])

    # set the index for writing
    param_df.set_index("Parameter",drop=True,inplace=True)
    assertion_df.set_index("ID",drop=True,inplace=True)

    # write assertions to CSV
    param_df.to_csv("gbif_fields.csv",mode="w")
    assertion_df.to_csv("gbif_assertions.csv",mode="w")
                                  
if __name__ == "__main__":
    main()