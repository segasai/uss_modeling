# Unofficial USS modeler

*use at your own risk*


The routines to help understand the USS modeling and its value
as well as proposed changes


At the moment useful tools include utils.future_value which computes
the expected DB, DC and lump sumps for a given salary and time in years
to retirement.

I.e.

```python

# proposed USS changes with inflation of 2.5%
In [138]: print ('DB,DC,Lump', utils.future_value(60, 66 - 38, salary_inc=0.04,
     ...: uss_options =utils.USS_NEW_opts, inflation=0.025))
DB,DC,Lump (12.855093256814921, 362.6697541407869, 38.565279770444754)

# old USS
In [139]: print ('DB,DC,Lump', utils.future_value(60, 66 - 38, salary_inc=0.04,
     ...: uss_options =utils.USS_OLD_opts, inflation=0.025))
DB,DC,Lump (21.811280650406506, 122.53846135713475, 65.4338419512195)

# proposed USS changes with inflation 5%
In [140]: print ('DB,DC,Lump', utils.future_value(60, 66 - 38, salary_inc=0.04,
     ...: uss_options =utils.USS_NEW_opts, inflation=0.05))
DB,DC,Lump (6.547011270904586, 184.70523087937735, 19.641033812713754)

# old USS with inflation 5%
In [141]: print ('DB,DC,Lump', utils.future_value(60, 66 - 38, salary_inc=0.04,
     ...: uss_options =utils.USS_OLD_opts, inflation=0.05))
DB,DC,Lump (18.802511627423236, 0.047417364024311695, 56.407534882269715)

```

Currently the numbers come from the the changes that USS plans to adopt from next year.
The inflation and stock market growth are free parameters of the tool


Pull requests,bug fixes are encouraged
