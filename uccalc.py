"Write out file with credit for all combinations of 8 inputs"

import os
import sys
import csv

# there are 8 pssible inputs. Here are their discrete values

FAMILY_COMPOSITION_OPTIONS = [1, 2]
FC_SINGLE = 1
FC_COUPLE = 2


# if one person in family, 1/2/3; if couple, 1/2/34/5/6 possible
CAPACITY_FOR_WORK_OPTIONS = [1,2,3,4,5,6]
CW_ELEMENT = {
        1: 0,       # Able to work
        2: 146.12,  # One limited capacity to work
        3: 358.93,  # One limited capacity to work RA
        4: 146.12,  # Both LCW
        5: 358.93,  # One LCW and One LCWRA
        6: 358.93   # Both LCWRA
    }


CA_UNDER25 = 1 # both aged under 25
CA_OVER25 = 2 # one or both over 25



def basic_element(family_composition, claimant_ages):
    if family_composition == FC_SINGLE:
        if claimant_ages ==CA_UNDER25:
            return 291.73
        else:
            return 368.25
    else: # couple
        if claimant_ages == CA_UNDER25:
            return 457.93
        else:
            return 578.07




def calculate_allowances(
        family_composition,
        capacity_for_work,
        claimant_ages,
        number_of_able_children=0,
        number_of_disabled_children=0,
        number_of_severely_disabled_children=0,
        full_time_carer=False,
        claims_for_housing_costs=True
    ):
    "Work out a pair of numbers for this case with max max_monthly_entitlement and work_allowance"

    el_basic = basic_element(family_composition, claimant_ages)

    el_lcw = CW_ELEMENT[capacity_for_work]

    kids = number_of_able_children + number_of_disabled_children + number_of_severely_disabled_children
    if kids == 0:
        el_child = 0
    elif kids == 1:
        el_child = 321.60
    else:
        el_child = 321.60 + (kids - 1) * 267.92

    el_disabled = (146.12 * number_of_disabled_children) + (417.15 * number_of_severely_disabled_children)

    el_carer = (full_time_carer and 171.04 or 0.0)

    mme = el_basic + el_lcw + el_child + el_disabled + el_carer

    
    work_allowance = 0


    if (family_composition == FC_SINGLE) and (kids == 0):
        work_allowance = 131.20

    if (family_composition == FC_COUPLE) and (kids == 0):
        work_allowance = 131.20

    if (family_composition == FC_COUPLE) and (kids > 0) and claims_for_housing_costs:
        work_allowance = 262.40

    if (family_composition == FC_COUPLE) and (kids > 0) and not claims_for_housing_costs:
        work_allowance = 633.55

    if (family_composition == FC_SINGLE) and (kids > 0) and claims_for_housing_costs:
        work_allowance = 310.87

    if (family_composition == FC_SINGLE) and (kids > 0) and claims_for_housing_costs:
        work_allowance = 867.59

    if (capacity_for_work != 1) and (kids == 0) and claims_for_housing_costs:
        work_allowance = 226.94

    if (capacity_for_work != 1) and (not claims_for_housing_costs) and not ((family_composition == FC_COUPLE) and (kids > 0)):
        work_allowance = 764.75



    return (mme, work_allowance)



def generate_combinations_file():
    "Output all combinations of inputs"
    outfilename = "combinations.csv"
    colnames = ["Composition", "Capacity", "Ages", "AbleKids", "DisabledKids", "SevereKids", "Carer", "Housing", "MaxME", "WAllow"]


    with open(outfilename, 'w') as csvfile:
        w =  csv.writer(csvfile)
        w.writerow(colnames)
        combinations = 0
        for family_composition in [FC_SINGLE, FC_COUPLE]:
            if family_composition == FC_SINGLE:
                workoptions = [1,2,3]
            else:
                workoptions = [1,2,3,4,5,6]
            for capacity_for_work in workoptions:
                for claimant_ages in [CA_UNDER25, CA_OVER25]:

                    for carer in [True, False]:
                        for claims_housing in [True, False]:

                    # 
                            # generate randome numbers of kids either able, moderately disabled or severly disable.
                            # discard cases where total is more than 10.
                            for ablekids in range(11):
                                for somewhatdisabledkids in range(11):
                                    for severelydisabledkids in range(11):

                                        # assume max 10 kids; 30 would be a bit silly (although lucrative)
                                        if (ablekids + somewhatdisabledkids + severelydisabledkids) > 10:
                                            continue


                                        max_monthly_entitlement, work_allowance = calculate_allowances(
                                            family_composition,
                                            capacity_for_work,
                                            claimant_ages,
                                            ablekids,
                                            somewhatdisabledkids,
                                            severelydisabledkids,
                                            carer,
                                            claims_housing
                                            )


                                        row = [family_composition, capacity_for_work, claimant_ages, 
                                            ablekids, somewhatdisabledkids, severelydisabledkids,
                                            carer, claims_housing,
                                            '%0.2f' % max_monthly_entitlement, '%0.2f' % work_allowance
                                            ]
                                        w.writerow(row)
                                        combinations += 1

        print("Wrote %s with %d combinations of inputs" % (outfilename, combinations))

if __name__=='__main__':
    generate_combinations_file()


