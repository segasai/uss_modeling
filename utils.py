import numpy as np
import scipy.optimize


class InflationCap:
    """ Inflation capping """
    def __init__(self, x1, x2):
        self.x1 = x1
        self.x2 = x2

    def __call__(self, x):
        """ Compute the inflation with the cap
        use official pension formula
        """
        if x < self.x1:
            return self.x
        if (x > self.x1) & (x.self < self.x2):
            return (x - self.x1) * .5 + self.x1
        if (x > self.x2):
            return (self.x2 - self.x1) * .5 + self.x1


# proposed USS parameters
USS_NEW_opts = dict(db_cut=40,
                    empee_contribution_perc1=0.098,
                    empee_contribution_perc2=0.08,
                    empyer_contribution_perc1=0.214,
                    empyer_contribution_perc2=0.12,
                    db_accr_rate=1. / 85,
                    lump_frac=3. / 85,
                    inflation_cap=InflationCap(0.025, 0.025))

# OLD USS parameters
USS_OLD_opts = dict(db_cut=59.88365,
                    empee_contribution_perc1=0.096,
                    empee_contribution_perc2=0.08,
                    empyer_contribution_perc1=0.214,
                    empyer_contribution_perc2=0.12,
                    db_accr_rate=1. / 75,
                    lump_frac=3. / 75,
                    inflation_cap=InflationCap(0.5, 0.15))

# inflation cap not quite right because of the


def income_tax(yearly_salary):
    """
    Compute the income tax given yearly salary in kGBP
    """
    bands = [0, 12.57, 50.27, 150, np.inf]
    percents = [0, 0.2, 0.4, .45]

    tax = 0
    for i in range(len(bands) - 1):
        if (yearly_salary > bands[i]):
            tax += max(
                (min(yearly_salary, bands[i + 1]) - bands[i]) * percents[i], 0)
    return tax


def ni_tax(yearly_salary):
    """
    Compute ni tax given salary in kGBP
    """
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
                        empee_contribution_perc1=0.098,
                        empee_contribution_perc2=0.08,
                        **kwargs):
    """
    How much the salary will decrease due to uss contribution 
    this is pre tax
    """
    val = min(salary, db_cut) * empee_contribution_perc1 + max(
        0, salary - db_cut) * empee_contribution_perc2
    return val


def uss_benefits(salary,
                 db_cut=40,
                 empee_contribution_perc1=0.098,
                 empee_contribution_perc2=0.08,
                 empyer_contribution_perc1=0.214,
                 empyer_contribution_perc2=0.12,
                 db_accr_rate=1. / 85,
                 lump_frac=3. / 85):
    """
    return current value uss benefits -- tuple of DB/DC/LUMP
    """
    below_cut = min(salary, db_cut)
    above_cut = max(salary - below_cut, 0)

    db_benefit = db_accr_rate * below_cut
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
                 inflation_cap=0.025,
                 db_cut0=40):
    """
    Return DB, DC value at retirement in todays GBP

    Parameters
    ----------
    salary0: float
         Current yearly salary
    delta_years: integer
         How many years before pension
    inflation: float
         Fractional inflation i.e. 0.035 for 3.5%
    salary_inc: float
         Fractional Salary increase per year
    stock_market: float
         Fractional growth of stock market per year
    inflation_cap: float
         USS cap on inflation (proposed 0.025)
    db_cut0: float
         Current boundary between DB/DC contribution (i.e. 40)
    
    """
    db_cut = db_cut0
    accum_db, accum_dc, accum_lump = 0, 0, 0
    for year in range(delta_years):
        salary = salary0 * (salary_inc + 1)**year
        # yearly salary increase

        # the existing DB and lump is scaled by inflation up to a cap
        accum_db = (min(inflation, inflation_cap) + 1) * accum_db
        accum_lump = (min(inflation, inflation_cap) + 1) * accum_lump

        # DC just grows as stock market
        accum_dc = (1 + stock_market) * accum_dc
        # compute current year benefits they are appended
        db, dc, lump = uss_benefits(salary, db_cut=db_cut)
        accum_db += db
        accum_dc += dc
        accum_lump += lump

        # the threshold for DB/DC is also updated each year
        db_cut = db_cut * (min(inflation, inflation_cap) + 1)

    # recompute now them in today's GBP
    accum_db, accum_dc, accum_lump = [
        _ / (1 + inflation)**delta_years
        for _ in [accum_db, accum_dc, accum_lump]
    ]
    return accum_db, accum_dc, accum_lump


def annuity_rate():
    # based on USS calculator
    # How much you have to pay for an annuity (at pension age)

    return 0.025
