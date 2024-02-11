import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib
from scipy.stats import pearsonr


def count_professionals_by_authority(med_serv_table: pd.DataFrame, profession: str = None, kupa: str = None) -> pd.Series:
    """"
    this function filters the med_serv_table according to the required profession and/or kupat-holim
    and then grouped the data by the local authority.
    :param med_serv_table: a pandas dataframe containing all medical doctors in Israel including their profession and
    address
    :param profession: string, the specific profession we want to filter the table by. default is None, which means that all
    professions will be included
    :param kupa: string, the specific kupat-holim we want to filter the table by. default is None, which means that all
    kupat-holim will be included
    """
    profession_table = med_serv_table
    if profession is not None:
        profession_table = med_serv_table[med_serv_table["סוג התמחות"] == profession]
    if kupa is not None:
        profession_table = profession_table[profession_table["קופת חולים"] == kupa]
    profession_table_grouped = profession_table.groupby("עיר").nunique()["שם"].rename("num docs")

    return profession_table_grouped


def merge_professionals_and_population(professional_table_grouped: pd.DataFrame, local_auth_table: pd.DataFrame,
                                       local_auth_population_col: str)-> pd.DataFrame:
    """
    this function merges the following two tables: 1. medical services table grouped by local authority 2. local authorities
    table that includes population information by authority. these two tables are merged based on the local authority
     column which is actually assumed to be the index of the two tables
    :param professional_table_grouped: pandas series whose index is local authorities it is an output of grouping a
     medical services table
    :param local_auth_table: pandas dataframe whose index is local authorities.
    :param local_auth_population_col: name of the column containing the relevant population information in the
     local_auth_table
    :return: pd.Dataframe whose is a merge between population information from the local authorities table and doctors
    count per local authority from the medical services table
    """
    merged_table = pd.merge(pd.DataFrame(local_auth_table[local_auth_population_col]),
                            professional_table_grouped,
                            how="inner", left_index=True, right_index=True)

    return merged_table


def gen_correlation_plot(merged_table: pd.merge, local_auth_population_col: str, profession: str = None,
                         xlabel: str = None, ylabel:str = None, title:str = None, print_corr: bool = True, ax=None,
                         **kwargs)->matplotlib.axes:
    """
    this function generates a correlation plot between population information from the local authorities table and
    doctors count from the medical services table
    :param merged_table: pd.Dataframe whose is a merge between population information from the local authorities table and doctors
    count per local authority from the medical services table
    :param local_auth_population_col: name of the column containing the relevant population information in the
     local_auth_table
    :param profession: string, the specific profession we want to filter the table by. default is None, which means that all
    professions will be included
    :param xlabel: string, the x label for the plot
    :param ylabel: string, the y label for the plot
    :param title: string, the title for the plot
    :param print_corr: boolean, whether to include the pearson r and p values in the plot
    :param ax: pre-defined plot axes, if none, a new one will be created
    :param kwargs: kwargs passed to matplotlib.pyplot
    :return: matplotlib axes object
    """
    if ax is None:
        fig, ax = plt.subplots()

    ax.scatter(merged_table[local_auth_population_col], merged_table["num docs"], **kwargs)
    xlabel = xlabel if xlabel is not None else local_auth_population_col
    ylabel = ylabel if ylabel is not None else "num docs"
    title = title if title is not None else f"correlation between {local_auth_population_col} and {profession}"

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    if print_corr:
        r, p = pearsonr(merged_table[local_auth_population_col], merged_table["num docs"])
        ax.text(0.01, 0.99, f"Pearson r={round(r, 3)}, p={round(p, 3)}", va="top", ha="left", transform=ax.transAxes)

    return ax


def gen_med_service_correlation_plot(med_serv_table: pd.DataFrame, local_auth_table: pd.DataFrame,
                                     local_auth_population_col: str,
                                     profession: str = None, kupa: str = None,
                                     xlabel: str = None, ylabel: str = None, title: str = None, print_corr: bool = True,
                                     ax = None, **plot_kwargs):
    """
    this function is the interface function. it calls other function to execute the following sequence: 1. group the
    medical services table by local authorities 2. merge the grouped output with population information from the local
    authority table. 3. plot the correlation between local authorities' population and the doctor counts
    :param med_serv_table: a pandas dataframe containing all medical doctors in Israel including their profession and
    address
    :param profession: string, the specific profession we want to filter the table by. default is None, which means that all
    professions will be included
    :param kupa: string, the specific kupat-holim we want to filter the table by. default is None, which means that all
    kupat-holim will be included
    :param local_auth_table: pandas dataframe whose index is local authorities.
    :param local_auth_population_col: name of the column containing the relevant population information in the
     local_auth_table
    :param xlabel: string, the x label for the plot
    :param ylabel: string, the y label for the plot
    :param title: string, the title for the plot
    :param print_corr: boolean, whether to include the pearson r and p values in the plot
    :param ax: pre-defined plot axes, if none, a new one will be created
    :param kwargs: kwargs passed to matplotlib.pyplot
    :return: matplotlib axes object
    """

    professional_table_grouped = count_professionals_by_authority(med_serv_table, profession=profession,
                                                                  kupa=kupa)

    merged_table = merge_professionals_and_population(professional_table_grouped, local_auth_table,
                                                      local_auth_population_col)

    ax = gen_correlation_plot(merged_table=merged_table, local_auth_population_col=local_auth_population_col,
                              profession=profession,
                              xlabel=xlabel, ylabel=ylabel, title=title, print_corr=print_corr, ax=ax,
                              **plot_kwargs)

    return ax