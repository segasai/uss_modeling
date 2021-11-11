# Unofficial USS modeler

*use at your own risk*


The routines to help understand the USS modeling and its value
as well as proposed changes


At the moment useful tools include utils.future_value which computes
the expected DB, DC and lump sumps for a given salary and time in years
to retirement.

I.e.

```
In [110]: print ('DB,DC,Lump', utils.future_value(60, 66 - 38, inflation=0.035,
     ...: salary_inc=0.04))
DB,DC,Lump (9.795208128888916, 276.3438314209598, 29.38562438666674)
```

Currently the numbers come from the the changes that USS plans to adopt from next year.
The inflation and stock market growth are free parameters of the tool


Pull requests,bug fixes are encouraged
