# from atlas_counts()

"""

# create payload (for ALA)
payload = {}

# check for Australian atlas
if atlas in ["Australia","ALA"]:

    # check for data profile first
    if use_data_profile:

        # add data quality profile directly to URL
        data_profile_list = list(show_all(profiles=True)['shortName'])
        baseURL = apply_data_profile(baseURL=baseURL,data_profile_list=data_profile_list)

    # else, disable all quality filters
    else:

        baseURL += "?disableAllQualityfilters=true&"

    # create payload
    payload = add_to_payload_ALA(payload=payload,atlas=atlas,taxa=taxa,filters=filters,
                                    polygon=polygon,bbox=bbox,scientific_name=scientific_name,
                                    simplify_polygon=simplify_polygon)

    # try this for payload
    if payload is None:
        return None

    # check for group by
    if group_by is not None:

        # get grouped table
        return galah_group_by(URL=baseURL,method=method,group_by=group_by, filters=filters, verbose=verbose, total_group_by=total_group_by,payload=payload)

    # create the query id
    qid_URL, method2 = get_api_url(column1="api_name",column1value="occurrences_qid")

    # add options for data quality profiles
    if use_data_profile:
        data_profile_list = list(show_all(profiles=True)['shortName'])
        qid_URL = apply_data_profile(baseURL=qid_URL,data_profile_list=data_profile_list)
    else:
        qid_URL += "?disableAllQualityfilters=true&"

    # cache the user's query and get a query ID
    qid = requests.request(method2,qid_URL,data=payload,headers=headers)
    print(qid)

    # create the URL to grab your queryID and counts
    URL = baseURL + "fq=%28qid%3A" + qid.text + "%29&flimit=-1&pageSize=0"

    if verbose:
        print()
        print("headers: {}".format(headers))
        print()
        print("payload for queryID: {}".format(payload))
        print("queryID URL: {}".format(qid_URL))
        print("method: {}".format(method2))
        print()
        print("qid for query: {}".format(qid.text))
        print("URL for result:{}".format(URL))
        print("method: {}".format(method))
        print()

    # get data
    response = requests.request(method,URL,headers=headers)

    # check for daily maximum
    if response.status_code == 429:
        raise ValueError("You have reached the maximum number of daily queries for the ALA.")

    # get data from response
    response_json = response.json()

    # return dataFrame with total number of records
    return pd.DataFrame({'totalRecords': [response_json[COUNTS_NAMES[atlas]]]})

else:
"""

# atlas_media()
"""
    # create the output data frame
    if atlas == "Australia":
        data_columns = {
            "decimalLatitude": [],
            "decimalLongitude": [],
            "eventDate": [],
            "scientificName": [],
            "recordID": [],
            "dataResourceName": [],
            "occurrenceStatus": [],
            "multimedia": [],
            "imageIdentifier": [],
            "mimeType": [],
            "sizeInBytes": [],
            "dateUploaded": [],
            "dateTaken": [],
            "height": [],
            "width": [],
            "creator": [],
            "license": [],
            "dataResourceUid": [],
            "occurrenceID": [],
        }
    elif atlas == "Austria":
        data_columns = {
            "decimalLatitude": [],
            "decimalLongitude": [],
            "eventDate": [],
            "scientificName": [],
            "recordID": [],
            "occurrenceStatus": [],
            "multimedia": [],
            "imageIdentifier": [],
            "mimeType": [],
            "sizeInBytes": [],
            "dateUploaded": [],
            "dateTaken": [],
            "height": [],
            "width": [],
            "creator": [],
            "license": [],
            "dataResourceUid": [],
            "occurrenceID": [],
        }
    else:
        raise ValueError("Atlas {} is not taken into account".format(atlas))

    # for if the user wants to collect the urls
    image_urls = []
"""

# atlas_occurrences()
"""
if atlas in ["Australia","ALA"]:
    
    # check for assertions and lump them with filters, as filters takes care of these
    if filters is not None and assertions is not None:
        if type(assertions) is list:
            filters += assertions
        else:
            filters.append(assertions)
    elif filters is None and assertions is not None:
        filters=assertions

    # create payload
    payload = add_to_payload_ALA(payload=payload,atlas=atlas,taxa=taxa,filters=filters,polygon=polygon,
                                bbox=bbox,simplify_polygon=simplify_polygon,scientific_name=scientific_name)
    
    # try this for payload
    if payload is None:
        return None

    # create the query id
    qid_URL, method2 = get_api_url(column1="api_name",column1value="occurrences_qid")
    qid = requests.request(method2,qid_URL,data=payload,headers=headers)
    
    # create the URL to grab your queryID and counts
    if use_data_profile:
        data_profile_list = list(show_all(profiles=True)['shortName'])
        baseURL = apply_data_profile(baseURL=baseURL,data_profile_list=data_profile_list)   

    # Add qa=None to not get any assertions 
    if fields is None:
        selected_fields = galah_select(select="basic",atlas=atlas)
        if mint_doi: 
            URL = baseURL + "fq=%28qid%3A" + qid.text + "%29&" + selected_fields + "&qa=none&flimit=-1&mintDoi=TRUE"
        else:
            URL = baseURL + "fq=%28qid%3A" + qid.text + "%29&" + selected_fields + "&qa=none&flimit=-1"
    elif fields == "all":
        if mint_doi:
            URL = baseURL + "fq=%28qid%3A" + qid.text + "%29&qa=none&flimit=-1&mintDoi=TRUE"
        else:
            URL = baseURL + "fq=%28qid%3A" + qid.text + "%29&qa=none&flimit=-1"
    else:
        # print("am I here?")
        if mint_doi:
            URL = baseURL + "fq=%28qid%3A" + qid.text + "%29&" + galah_select(select=fields,atlas=atlas) + "&qa=none&flimit=-1&mintDoi=TRUE"
        else:
            URL = baseURL + "fq=%28qid%3A" + qid.text + "%29&" + galah_select(select=fields,atlas=atlas) + "&qa=none&flimit=-1"

    if verbose:
        print()
        print("headers: {}".format(headers))
        print("payload for queryID: {}".format(payload))
        print("queryID URL: {}".format(qid_URL))
        print("method: {}".format(method2))
        print()
        print("qid for query: {}".format(qid.text))
        print("URL for result:{}".format(URL))
        print("method: {}".format(method))
        print()

    # get data
    response = requests.request(method,URL,headers=headers)   

else:
"""

# atlas_species()
"""
    # create payload variable so it is available for some atlases
    payload = {}
    
    if atlas in ["Australia","ALA"]:
        
        # create payload and add buffer to polygon if user specifies it
        payload = add_to_payload_ALA(payload=payload,atlas=atlas,taxa=taxa,filters=filters,polygon=polygon,
                                     bbox=bbox,simplify_polygon=simplify_polygon,scientific_name=scientific_name)

        # create the query id
        qid_URL, method2 = get_api_url(column1="api_name",column1value="occurrences_qid")
        qid = requests.request(method2,qid_URL,data=payload,headers=headers)
        
        # create the URL to grab the species ID and lists
        if use_data_profile:
            data_profile_list = list(show_all(profiles=True)['shortName'])
            baseURL = apply_data_profile(baseURL=baseURL,use_data_profile=use_data_profile,data_profile_list=data_profile_list)
            URL = baseURL + "fq=%28qid%3A" + qid.text + "%29&facets={}&lookup=True".format(rankID)
            if counts:
                URL += "&count=true"
        else:
            URL = baseURL + "?fq=%28qid%3A" + qid.text + "%29&facets={}&lookup=True".format(rankID)
            if counts:
                URL += "&count=true"

        if verbose:
            print()
            print("headers: {}".format(headers))
            print()
            print("payload for queryID: {}".format(payload))
            print("queryID URL: {}".format(qid_URL))
            print("method: {}".format(method2))
            print()
            print("qid for query: {}".format(qid.text))
            print("URL for result:{}".format(URL))
            print("method: {}".format(method))
            print()

        # get data
        response = requests.request(method,URL,headers=headers)

        # check for daily maximum
        if response.status_code == 429:
            raise ValueError("You have reached the maximum number of daily queries for the ALA.")
        
        # return data as pandas dataframe
        return pd.read_csv(io.StringIO(response.text))
"""

# search_taxa()
"""
    if atlas in ["Australia"] and len(taxa) > 10:

        baseURL, method = get_api_url(
            column1="called_by",
            column1value="atlas_species",
            column2="api_name",
            column2value="names_search_bulk_species",
        )
        payload = {"vernacular": "true", "names": [], "issues": "true"}
        payload["names"] = taxa  # [" OR ".join("lsid:{}".format(id) for id in taxa)]
        species_list_test = requests.request(method, baseURL, data=json.dumps(payload))
        # print(species_list_test.text)
        species_list_json = species_list_test.json()
        species_list_dataframe = pd.DataFrame(species_list_json)
        species_list_rename = species_list_dataframe.rename(
            columns={
                "identifier": "taxonConceptID",
                "classs": "class",
                "author": "scientificNameAuthorship",
                "acceptedConceptName": "scientificName",
                "name": "species",
                "commonName": "vernacularName",
            }
        )
        return species_list_rename[
            [
                "scientificName",
                "scientificNameAuthorship",
                "taxonConceptID",
                "rank",
                "kingdom",
                "phylum",
                "class",
                "order",
                "family",
                "genus",
                "species",
                "vernacularName",
            ]
        ]
"""

# galah_group_by
"""
if atlas in ["Australia","ALA"]:
    # try startingURL2
    #startingURL2,method = get_api_url(column1='called_by',column1value='atlas_counts',column2="api_name",
    #                            column2value="records_counts")

    # get response from your query, which will include all available fields
    qid_URL, method2 = get_api_url(column1="api_name",column1value="occurrences_qid")
    qid = requests.request(method2,qid_URL,data=payload,headers=headers)
    facets = "".join("&facets={}".format(g) for g in group_by)
    if startingURL[-1] == "&":
        URL = startingURL + "fq=%28qid%3A" + qid.text + "%29" + facets + "&flimit=-1&pageSize=0"
    else:
        URL = startingURL + "?fq=%28qid%3A" + qid.text + "%29" + facets + "&flimit=-1&pageSize=0"

    # check to see if the user wants the URL for querying
    if verbose:
        print()
        print("headers: {}".format(headers))
        print()
        print("payload for queryID: {}".format(payload))
        print("queryID URL: {}".format(qid_URL))
        print("method: {}".format(method2))
        print()
        print("qid for query: {}".format(qid.text))
        print("URL for result:{}".format(URL))
        print("method: {}".format(method))
        print()

    response = requests.request(method,URL,headers=headers)
    response_json = response.json()
    facets_array=[]

else:
"""
"""
if atlas in ["Australia","ALA"]:
    print()
    print("payload for queryID: {}".format(payload_for_querying))
    print("queryID URL: {}".format(qid_URL))
    print("method: {}".format(method2))
    print()
    print("qid for query: {}".format(qid.text))
    print("URL for result:{}".format(tempURL))
    print("method: {}".format(method))
    print()
else:
"""

"""
            # loop over each facet
            #for facet in f:
            if atlas in ["Australia","ALA"]:
            
                # check for fq in payload
                if "fq" not in payload:
                    payload["fq"] = [f]
                else:
                    payload["fq"].append(f)
                    
                payload_for_querying = copy.deepcopy(payload)
                
                # create payload and get qid
                qid_URL, method2 = get_api_url(column1="api_name",column1value="occurrences_qid")
                qid = requests.request(method2,qid_URL,data=payload,headers=headers)
                if startingURL[-1] == "&":
                    tempURL = startingURL + "fq=%28qid%3A" + qid.text + "%29" 
                else:
                    tempURL = startingURL + "?fq=%28qid%3A" + qid.text + "%29"
                if any("lsid" in fq for fq in payload['fq']):
                    index = [idx for idx, s in enumerate(payload['fq']) if 'lsid' in s][0]
                    payload["fq"] = [payload["fq"][index]]
                else:
                    payload["fq"] = []
                if filters is not None:
                    payload = add_to_payload_ALA(payload=payload,
                                                    atlas=atlas,
                                                    filters=filters)
                tempURL += "&facets={}".format(group_by[-1])
                
            else:
            """

"""
# galah_filter()
    # elif atlas in ["Australia","ALA"]:
    #     if specialChar == '=' or specialChar == '==':
    #         if parts[1].isdigit() and ifgroupBy:
    #             return "{}:{}".format(parts[0],parts[1])
    #         elif parts[1] == '':
    #             return "*:* AND -{}:*".format(parts[0])
    #         elif parts[1] == "True":
    #             return"assertions:{}".format(parts[0])
    #         elif parts[1] == "False":
    #             return "-assertions:{}".format(parts[0])
    #         else:
    #             # check if this is array
    #             arrayChars = re.compile('[]') # removed this: \[\]
    #             arrayChar = arrayChars.findall(parts[1])
    #             if arrayChar:
    #                 temp_array = parts[1][1:-1].split(",")
    #                 for value in temp_array:
    #                     # added quotes here
    #                     returnString += "{}:\"{}\" OR ".format(parts[0], value)
    #                 returnString = returnString[:-4]
    #                 return returnString
    #             else:
    #                 return "{}:\"{}\"".format(parts[0],parts[1])

    #     elif specialChar == '>':
    #         return "{}:[{} TO *] AND -({}:{})".format(parts[0], parts[1], parts[0], parts[1])

    #     # less than
    #     elif specialChar == '<':
    #         return "{}:[* TO {}] AND -({}:{})".format(parts[0], parts[1], parts[0], parts[1])

    #     # greater than or equal to
    #     elif specialChar == '=>' or specialChar == '>=':
    #         return "{}:[{} TO *]".format(parts[0], parts[1])

    #     # less than or equal to
    #     elif specialChar == '<=' or specialChar == '=<':
    #         return "{}:[* TO {}]".format(parts[0], parts[1])

    #     # not equal to
    #     elif specialChar == '!=' or specialChar == '=!':
    #         print("here")
    #         return "-{}:{}".format(parts[0], parts[1])

    #     # else, there is either an error in the filters or a missing case
    #     else:
    #         raise ValueError("The special character {} is not included in the filters function.  Either it is not a logical operator, or it has not been included yet.".format(specialChar[0]))


"""


"""
atlas_occurrences()

    # # test to check if atlas is working
    # requestURL, method = get_api_url(
    #     column1="called_by",
    #     column1value="atlas_counts",
    #     column2="api_name",
    #     column2value="records_counts",
    # )
    # requestURL += "?pageSize=0"

    # # check if the atlas is working - if not, let the user know
    # response = requests.request(method, requestURL, headers=headers)
    # try:
    #     response.raise_for_status()
    #     if test:
    #         return
    # except requests.exceptions.HTTPError as e:
    #     print("The {} atlas might be down...")
    #     print("Error: " + str(e))
    #     sys.exit()
"""
