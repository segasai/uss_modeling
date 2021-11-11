
The routines to help understand the USS modeling and its value
as well as proposed changes


At the moment useful tools include utils.future_value which computes
the expected DB, DC and lump sumps for a given salary and time in years
to retirement.

I.e.

```
print ('DB,DC,Lump', utils.future_value(60, 66 - 38, inflation=0.035))
DB,DC,Lump (21.783824632752452, 925.8102815212872, 65.3514738982574)
```

Currently the numbers come from the the changes that USS plans to adopt from next year.
The inflation and stock market growth are free parameters of the tool


Pull requests,bug fixes are encouraged