
The routines to help understand the USS modeling and its value
as well as proposed changes


At the moment useful tools include utils.future_value which computes
the expected DB, DC and lump sumps for a given salary and time to retirement.
I.e.


```
print ('DB,DC,Lump', utils.future_value(60,66-38))
Out[61]: (21.783824632752452, 925.8102815212872, 65.3514738982574)

```

Currently the numbers come from the the changes that USS plans to adopt from next year.


Pull requests,bug fixes are encouraged