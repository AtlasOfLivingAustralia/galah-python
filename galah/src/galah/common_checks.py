from .common_dictionaries import atlases
from .galah_config import readConfig


def check_atlas(atlas=None, function=None):
    """Check to see if the atlas the user provided is correct"""
    if atlas not in atlases:
        raise ValueError("Atlas {} not taken into account for the {} function".format(atlas, function))


def check_email_empty():
    configs = readConfig()

    if configs["galahSettings"]["email"] in [
        None,
        "",
        configs["galahSettings"]["email"] == "email@example.com",
    ]:
        raise ValueError("Please provide an email for querying.")


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
        raise ValueError("The taxa argument only takes a string or a list, not {}.".format(type(taxa)))

    # return taxa
    return taxa


def check_for_dict(variable=None, variable_name=None):
    if not isinstance(variable, dict):
        raise ValueError("Only a dictionary is accepted for {}.".format(variable_name))


def check_args_none(all_args=None):
    if all(x is None for x in all_args):
        raise ValueError("You need to specify one of the following:\n\n{}".format("\n".join(all_args)))


def check_args_specific_atlas(all_args=None, atlas=None, specific_atlases=None):
    names_all_args = [x.__name__ for x in all_args]
    print(names_all_args)
    if any(x is not None for x in all_args) and atlas not in specific_atlases:
        raise ValueError(
            "{} are only available for the {} atlas.".format("and".join(all_args), ",".format(specific_atlases))
        )
