#
# Sample Policy class definition
#


from polzybackend.policy import Policy
import policy_system


class SamplePolicy(Policy):

    # policy statuses with corresponded possible activities 
    activities_by_state = {
        'active': [
            'cancel',
            'suspend',
        ],
        'canceled': [],
        'suspended': [
            're-activate'
        ],
    }

    # policy attribute descriptions
    attributes_policy = {
        'Policy Attribute 1': 'Description of Policy Attribute 1',
        'Policy Attribute 2': 'Description of Policy Attribute 2',
        'Policy Attribute 3': 'Description of Policy Attribute 3',
        'Policy Attribute 4': 'Description of Policy Attribute 4',
    }

    # product line attribute descriptions
    attributes_product_line = {
        'Life': {
            'Life Attribute 1': 'Description of Life Attribute 1',
            'Life Attribute 2': 'Description of Life Attribute 2',
            'Life Attribute 3': 'Description of Life Attribute 3',
        },
        'Health': {
            'Health Attribute 1': 'Description of Health Attribute 1',
            'Health Attribute 2': 'Description of Health Attribute 2',
            'Health Attribute 3': 'Description of Health Attribute 3',
            'Health Attribute 4': 'Description of Health Attribute 4',
            'Health Attribute 5': 'Description of Health Attribute 5',
        },
        'P&C': {
            'P&C Attribute 1': 'Description of P&C Attribute 1',
            'P&C Attribute 2': 'Description of P&C Attribute 2',
        },
        'Car': {
            'Car Attribute 1': 'Description of Car Attribute 1',
        },
    }

    # insured person attribute descriptions
    attributes_insured_person = {
        'Insured Object Attribute 1': 'Description of Insured Object Attribute 1',
        'Insured Object Attribute 2': 'Description of Insured Object Attribute 2',
        'Insured Object Attribute 3': 'Description of Insured Object Attribute 3',
    }

    # insured object attribute descriptions
    attributes_insured_object = {
        'Insured Object Attribute 1': 'Description of Insured Object Attribute 1',
        'Insured Object Attribute 2': 'Description of Insured Object Attribute 2',
        'Insured Object Attribute 3': 'Description of Insured Object Attribute 3',
    }

    # insured object type attribute descriptions
    attributes_insured_object_type = {
        'House': {
            'Hause Attribute 1': 'Description of House Attribute 1',
        },
        'Car': {
            'Car Attribute 1': 'Description of Car Attribute 1',
            'Car Attribute 2': 'Description of Car Attribute 2',
        },
        'Factory': {
            'Factory Attribute 1': 'Description of Factory Attribute 1',
            'Factory Attribute 2': 'Description of Factory Attribute 2',
            'Factory Attribute 3': 'Description of Factory Attribute 3',
        },
        'Field': {
            'Field Attribute 1': 'Description of Field Attribute 1',
            'Field Attribute 2': 'Description of Field Attribute 2',
        },
        'Forest': {
            'Forest Attribute 1': 'Description of Forest Attribute 1',
        },
    }

    # implementation attribute descriptions
    attributes_implementation = {
        'Implementation Attribute 1': 'Description of Implementation Attribute 1',
        'Implementation Attribute 2': 'Description of Implementation Attribute 2',
    }

    def fetch(self):
        # fetch policy data from Policy Management System
        data = policy_system.get(self.number, self.effective_date)
        if data:
            # reshape data if needed
            self.data = data
            return True

        return False
