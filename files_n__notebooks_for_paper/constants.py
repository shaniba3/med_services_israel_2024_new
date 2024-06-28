

class PopulationAndInsured:


    israel_total_population_end_2022 = 9662037
    total_with_health_insurance = 9420200
    perc_insured_clalit = 0.512
    perc_insured_maccabi = 0.274
    perc_insured_leumit = 0.138
    perc_insured_meuhedet = 0.076
    clalit_total_2022 = perc_insured_clalit * total_with_health_insurance
    maccabi_total_2022 = perc_insured_maccabi * total_with_health_insurance
    leumit_total_2022 = perc_insured_leumit * total_with_health_insurance
    meuhedet_total_2022 = perc_insured_meuhedet * total_with_health_insurance

    kupot_total_insured_dict = {
        "כללית": clalit_total_2022,
        "מכבי": maccabi_total_2022,
        "לאומית": leumit_total_2022,
        "מאוחדת": meuhedet_total_2022
    }