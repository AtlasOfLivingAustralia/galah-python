import pandas as pd

import galah,datetime

# this function does X
def atlas_citation(df = None):

    # check if data frame is empty - test below code
    # if df is None or type(df) is not pd.DataFrame:
    if df is None:
        raise ValueError("Please provide a data frame generated from atlas_occurrences() to get a citation."
                         "  To ensure success, set mint_doi=True in atlas_occurrences()")

    # check if mint_doi was set to true.  If it was, can do this

    date = datetime.datetime.now()
    print("ALA occurrences download access from Python with galah " + galah.__version__ + "\n" +
          "(https://github.com/AtlasOfLivingAustralia/galah_python/) on " +  str(date.year) + "-" + str(date.month) + "-"
          + str(date.day) + "\nSearch URL: will add URL here later")

    #print("ALA occurrences download " + doi_from_data +
    #      "(https://github.com/AtlasOfLivingAustralia/galah_python/) on " + datetime.datetime.now()

    '''
    return("ALA occurrences download access from Python with galah {}\n"
    "\(https:\/\/github.com\/AtlasOfLivingAustralia\/galah_python\/\)"
    '''
    '''
    search_url <- attributes(data)$search_url
    return(glue("
                ALA occurrence download accessed from R with galah {galah_version_string()} \\
                (https://github.com/AtlasOfLivingAustralia/galah/) on \\
                {Sys.Date()}. 
                Search url: {search_url})
                "
    ))
  }
  search_url <- attributes(data)$search_url
  glue("
       ALA occurrence download {attributes(data)$doi}.
       Accessed from R with {galah_version_string()} \\
       (https://github.com/AtlasOfLivingAustralia/galah/) on {Sys.Date()}.
    '''