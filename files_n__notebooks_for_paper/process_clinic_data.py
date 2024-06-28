import pandas as pd

from files_n__notebooks_for_paper.constants import PopulationAndInsured


def basic_process_for_clinics_tables(original_clinics_table: pd.DataFrame, tight_or_soft: str ="soft"):
    """

    :param original_clinics_table: pandas dataframe, the original clinics table downloaded from https://imoh.maps.arcgis.com/
    :param tight_or_soft: "tight" to define duplicates two rows that are identical by main name (authorith name),
    expertise_name and name (doctor's name) even if different in all other fields. "soft" to define duplicates only when
    two rows are identical by the above parameters and also hmo_desc, validity_date and availability hours fields (sunday_mor
    etc)
    :return: processed clinics data table
    """

    df = original_clinics_table.copy()
    print("original table shape: ", df.shape)

    # drop duplicates according to subset of the columns:
    dup_cols_tight = [ 'Main name','expertise_desc', 'name' ]

    dup_cols_soft = ['city_desc', 'Main name', 'hmo_desc', 'expertise_desc', 'name', 'address',
                'sunday_mor', 'sunday_aft',
                'monday_mor', 'monday_aft', 'tuesday_mor', 'tuesday_aft',
                'wednesday_mor', 'wednesday_aft', 'thursday_mor', 'thursday_aft',
                'friday_mor', 'friday_aft', 'saturday_mor', 'saturday_aft', 'validity_date']
    if tight_or_soft == "soft":
        dup_cols = dup_cols_soft
    else:
        dup_cols = dup_cols_tight
    df = df.drop_duplicates(subset=dup_cols, keep="first")
    print("table shape after duplicate removal: ", df.shape)

    # remove non relevant data:
    non_relevant_expertise = ["לא רלוונטי", "שירותי משרד"]
    df = df[~df.expertise_desc.isin(non_relevant_expertise)]
    print("table shape after removing irrelevant rows: ", df.shape)

    return df


def calc_doctors_per_amount(clinics_table: pd.DataFrame, amount: int = 1000, kupa: str =None,
                            expertise_list: list = None, service_list: list = None):

    """
    this function calculate the ratio of doctors per amount of population. the doctors count can be defined by expertise,
    service an kupa.
    :param clinics_table: clinics table to use for calculation
    :param amount: the specific amount of population to calculate doctors per this amount
    :param kupa: kupat holim, if none - calculate for all
    :param expertise_list: list of strings, include only expertise that appear in the data
    :param service_list: list of strings, use "רופאים" for doctors. consider including also "יועצים ומנתחים"
    :return: the doctors per amount ratio
    """
    if service_list is not None:
        clinics_table = clinics_table[clinics_table.services_type_desc.isin(service_list)]

    if expertise_list is not None:
        clinics_table = clinics_table[clinics_table.expertise_desc.isin(expertise_list)]

    kupot_total_insured_dict = PopulationAndInsured.kupot_total_insured_dict
    if kupa is not None:
        clinics_table = clinics_table[clinics_table.kupa == kupa]
        total_insured = kupot_total_insured_dict[kupa]
    else:
        total_insured = PopulationAndInsured.total_with_health_insurance

    doctors_per_1000 = len(clinics_table) * amount / total_insured

    return doctors_per_1000








