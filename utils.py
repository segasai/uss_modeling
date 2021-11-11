import numpy as np
import scipy.optimize


def income_tax(yearly_salary):
    bands = [0, 12.57, 50.27, 150, np.inf]
    percents = [0, 0.2, 0.4, .45]

    tax = 0
    for i in range(len(bands) - 1):
        if (yearly_salary > bands[i]):
            tax += max(
                (min(yearly_salary, bands[i + 1]) - bands[i]) * percents[i], 0)
    return tax


def ni_tax(yearly_salary):
    weekly_salary = yearly_salary / 365 * 7
    bands = [0, .184, .967, np.inf]
    percents = [0, 0.12, 0.02]

    tax = 0
    for i in range(len(bands) - 1):
        if (weekly_salary > bands[i]):
            tax += (min(weekly_salary, bands[i + 1]) - bands[i]) * percents[i]

    tax = tax * 365 / 7  # rescale to year
    return tax


def uss_salary_decrease(salary,
                        db_cut=40,
                        contribution_perc1=0.098,
                        contribution_perc2=0.08):
    """
    How much the salary will decrease due to uss contribution 
    this is pre tax
    """
    val = min(salary, db_cut) * contribution_perc1 + max(
        0, salary - db_cut) * contribution_perc2
    return val


def uss_benefits(salary,
                 db_cut=40,
                 empee_contribution_perc1=0.098,
                 empee_contribution_perc2=0.08,
                 empyer_contribution_perc1=0.214,
                 empyer_contribution_perc2=0.12,
                 inv_accr_rate=85,
                 lump_frac=3. / 85):
    """
    return current value uss benefits -- tuple of DB/DC/LUMP
    """
    below_cut = min(salary, db_cut)
    above_cut = max(salary - below_cut, 0)

    db_benefit = 1. / inv_accr_rate * db_cut
    dc_benefit = (empee_contribution_perc2 +
                  empyer_contribution_perc2) * (above_cut)
    lump = lump_frac * below_cut
    return db_benefit, dc_benefit, lump


def sipp_tax_relief(salary):
    """ maximum tax relief for the sipp """

    bands = [0, 12.57, 50.27, 150, np.inf]
    amounts = []
    for i in range(len(bands) - 1):
        if salary > bands[i]:
            amounts.append(min(salary, bands[i + 1]) - bands[i])
        else:
            amounts.append(0)
    reliefs = [0, 0, 0.2, 0.25]
    max_relief = 0
    for a, r in zip(amounts, reliefs):
        max_relief += a * r
    return max_relief


def take_home(salary):
    """
    Return take home salary with USS,
    pair of (DB, DC) values,
    and the SIPP DC value is you would have left USS 
    """

    uss_pens = uss_salary_decrease(salary)
    inc_tax_val = income_tax(salary - uss_pens)
    ni_tax_val = ni_tax(salary - uss_pens)
    inc_tax_val0 = income_tax(salary)
    ni_tax_val0 = ni_tax(salary)
    # 1 / 0
    max_relief = sipp_tax_relief(salary)

    def func_find_pens(x):
        take1 = salary - uss_pens - inc_tax_val - ni_tax_val
        take2 = salary - x - inc_tax_val0 - ni_tax_val0 + max_relief
        return take1 - take2

    ret = scipy.optimize.bisect(func_find_pens, 0, salary)
    sipp_dc = ret
    uss_ben = uss_benefits(salary)
    return salary - uss_pens - inc_tax_val - ni_tax_val, uss_ben, sipp_dc


def future_value(salary0,
                 delta_years,
                 inflation=0.035,
                 salary_inc=0.04,
                 stock_market=0.08,
                 inflation_cap=0.025):
    """
    Return DB, DC value

    """
    accum_db, accum_dc, accum_lump = 0, 0, 0
    for year in range(delta_years):
        salary = salary0 * (salary_inc + 1)**year
        accum_db = (max(inflation, inflation_cap) + 1) * accum_db
        accum_dc = accum_dc * (1 + stock_market)
        accum_lump = (max(inflation, inflation_cap) + 1) * accum_lump
        db, dc, lump = uss_benefits(salary)
        accum_db += db
        accum_dc += dc
        accum_lump += lump

    return accum_db, accum_dc, accum_lump