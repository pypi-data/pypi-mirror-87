# Arbitrary precision decimal numbers

A module with a simple implementation for arbitrary precision
decimal numbers. The key difference to most other `decimal`
libraries is that there is no maximum precision for example
when doing divisions.

```
>>> from dezimal import Dec
>>> Dec("355") / Dec("113")
Dec('3.14159292035398230088495575221238938053097345132743362831858407079646017699115044247787610619469026548672566371681')
```

`dezimal` will calculate as many digits after the decimal point as
there are, no `ROUNDING_MODE` or whatever needed.

If the calculation
would result in a period, `dezimal` detects that and stops the calculation
as needed:

```
>>> Dec("1") / Dec("7")
Dec('0.14285714285714285')
```

However, it prints a minimum number of digits, as to display at least
the same precision as a regular `float` would (a bit more actually).

```
>>> Dec("1") / Dec("3")
Dec('0.33333333333333333')
>>> 1.0 / 3.0
0.3333333333333333
```

These parameters can be controlled by invoking the static `div`
method in `Dec` directly:

```
>>> Dec.div(Dec("1"), Dec("3"), minscale=5)
Dec('0.33333')
```

Also a maximum precision can be given:

```
>>> Dec.div(Dec("355"), Dec("113"), maxscale=30)
Dec('3.141592920353982300884955752212')
```


## Construction

An instance of `Dec` can be constructed from `int`, `float`, `bool`,
or a `str`. The usual formats like `3`, `3.0`, `7e1`, `-7e-9`, or
`+13.03e-3` are understood. 


## Supported operations

The following operations are supported:

```+ - * / // < <= > >= == !=```


## Why?

For fun.
