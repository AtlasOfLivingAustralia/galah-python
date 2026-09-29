def check_string_list(variable=None, variable_name=None):

    if variable is not None and not isinstance(variable, (list, str)):
        raise ValueError("Please provide a string or list for {}".format(variable_name))

    if isinstance(variable, str):
        return [variable]

    if isinstance(variable, list):
        for x in variable:
            if not isinstance(x, str):
                raise ValueError("All filters should be strings.")

    return variable


def check_taxa_type(taxa=None):

    # check to see if taxa is string or list
    if isinstance(taxa, (list, str)):

        # convert to list for easy looping
        if type(taxa) is str:
            taxa = [taxa]

    else:
        raise ValueError(
            "The taxa argument only takes a string or a list, not {}.".format(
                type(taxa)
            )
        )

    # return taxa
    return taxa


def check_for_dict(variable=None, variable_name=None):
    if not isinstance(variable, dict):
        raise ValueError("Only a dictionary is accepted for {}.".format(variable_name))


def check_args_none(all_args=None, names_all_args=None):
    if all(x is None for x in all_args):
        raise ValueError(
            "You need to specify one of the following:\n\n{}".format(
                "\n".join(names_all_args)
            )
        )


def check_args_specific_atlas(
    all_args=None, names_all_args=None, atlas=None, specific_atlases=None
):
    if any(x is not None for x in all_args) and atlas not in specific_atlases:
        raise ValueError(
            "{} are only available for the {} atlas(es).".format(
                ", ".join(names_all_args), ", ".join(specific_atlases)
            )
        )


def check_atlas_authenticate(atlas=None, authenticate=None):
    if atlas not in ["Australia", "ALA"] and authenticate:
        raise ValueError("Authentication is only available for the Australian atlas.")


def check_atlas_data_profile(atlas=None, use_data_profile=False):
    # raise error if argument is wrong type and/or the atlas doesn't have a quality profile but the user has specified one
    if use_data_profile and atlas not in ["Australia", "ALA"]:
        raise ValueError(
            "True and False are the only values accepted for data_profile, and the only atlas using a data \n"
            "quality profile is Australia.  Your atlas and data profile is \n"
            "set in your config file.  To set your default filter, find out what profiles are on offer:\n"
            "profiles = galah.show_all(profiles=True)\n\n"
            "and then type\n\n"
            "profiles['shortName']\n\n"
            "to get the names of the data quality profiles you can use.  To set a data profile, type\n"
            'galah.galah_config(data_profile="NAME FROM SHORTNAME HERE")'
            "If you don't want to use a data quality profile, set it to None by typing the following:\n\n"
            'galah.galah_config(data_profile="None")'
        )


def check_max_queries_ALA(response=None):
    # check for daily maximum
    if response.status_code == 429:
        raise ValueError(
            "You have reached the maximum number of daily queries for the ALA."
        )
