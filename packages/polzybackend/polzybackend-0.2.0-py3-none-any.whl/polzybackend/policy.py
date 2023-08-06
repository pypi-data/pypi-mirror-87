from datetime import datetime
import uuid


class Policy:
    #
    # Policy details, activities, attributes 
    #

    def __init__(self, number, date):
        #
        # initialization
        #

        self.id = uuid.uuid4()
        self.number = number
        self.effective_date = date
        self.data = None
        self.user = None

    @property
    def uuid(self):
        return str(self.id)

    def set_user(self, user):
        self.user = user

    def setStage(self, stage):
        self.stage = stage

    def setLanguage(self, language):
        self.language = language

    def fetch(self):
        #
        # IMPORTANT: this method should be define within custon implementation
        #
        # fetches policy details from Policy Management System
        #

        raise Exception('Fetch method is not set in policy class')

    def executeActivity(self, data):
        #
        # IMPORTANT: this method should be define within custon implementation
        #
        # executes policy activity defined in data
        #

        raise Exception('Execute Activity method is not set in policy class')

    def get(self):
        #
        # returns Policy data
        #

        result = {'id': self.uuid}
        if self.data:
            result.update(self.data)

        return result

    
    #def get_status(self):
    #    #
    #    # returns status of policy
    #    #
    #    if self.data:
    #        return self.data.get('status')

    #def get_product_line(self):
    #    #
    #    # returns name of policy's product line
    #    #
    #
    #    if self.data and self.data.get('product_line'):
    #        return self.data.prosuct_line.get('name')

    #def get_insured_is_person(self):
    #    #
    #    # returns:
    #    # - True if insured person
    #    # - False if insured object
    #    # - None otherwise
    #    #
    #
    #    if self.data and self.data.get('insured_object'):
    #        return self.data['insured_object'].get('is_person')

    #def get_insured_object_type(self):
    #    #
    #    # returns type of insure object
    #    #
    #
    #    if self.get_insured_is_person() is False:
    #        return self.data['insured_object'].get('type')


    #def get_possible_activities(self):
    #    #
    #    # returns list of possible activitites for policy
    #    #
    #
    #    return self.activities_by_state.get(self.get_status())

    #def get_attribute_descriptions(self):
    #    #
    #    # returns name-description of attributes applicable to policy 
    #    #
    #
    #    return {
    #        'policy': self.attributes_policy,
    #        'product_line': self.attributes_product_line.get(self.data['product_line'].get('name')),
    #        'insured_object': self.attributes_insured_person if self.get_insured_is_person() else self.attributes_insured_object,
    #        'insured_object_type': self.attributes_insured_object_type.get(self.get_insured_object_type()),
    #        'implementation': self.attributes_implementation,
    #    }

    
