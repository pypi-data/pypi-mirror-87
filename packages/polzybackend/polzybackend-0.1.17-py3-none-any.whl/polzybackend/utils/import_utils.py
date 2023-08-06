from flask import current_app
from importlib import import_module
from polzybackend.policy import Policy
from polzybackend.models import Activity


def import_class(name):
    #
    # imports class from string 'name' 
    #

    components = name.split('.')
    module_name = '.'.join(components[:-1])
    mod = import_module(module_name)
    cls = getattr(mod, components[-1])
    return cls


def get_policy_class():
    #
    # returns policy class
    #

    if current_app.config.get('CLASSNAME_POLICY'):
        return import_class(current_app.config.get('CLASSNAME_POLICY'))

    return Policy


def get_activity_class(activity_type_class):
    #
    # returns activity class
    #

    if current_app.config.get(activity_type_class):
        return import_class(current_app.config.get(activity_type_class))

    return Activity


def get_all_stages():
    #
    # returns list of all stages
    #

    if current_app.config.get('METHOD_GET_STAGES'):
        lClass = import_class(current_app.config.get('METHOD_GET_STAGES'))()
        return lClass.getAllStages
        # return import_class(current_app.config.get('METHOD_GET_STAGES'))

    raise Exception('Method to Get Stages NOT defined')
