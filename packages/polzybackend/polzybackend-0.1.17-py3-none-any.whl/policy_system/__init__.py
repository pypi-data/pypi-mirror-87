#
# emulator of a Policy Management System
#
import json
from time import sleep

DELAY_SECONDS = 5
POLICY_DATASET = 'policy_system/data/policies.json'

def get(policy_number, effective_date):
    #
    # returns policy from dataset
    #

    # load policies
    with open(POLICY_DATASET, 'r') as f:
        policies = json.load(f)
        # delay emulation
        sleep(DELAY_SECONDS)
        request_number = policy_number.upper().replace('-', '')
        request_date = effective_date.replace('-', '')
        print(f'**** REQUEST POLICY: {request_number} {request_date}')
        for item in policies:
            if request_number == item['number'].replace('-', '') and request_date == item['effective_date'].replace('-', ''):
                return item