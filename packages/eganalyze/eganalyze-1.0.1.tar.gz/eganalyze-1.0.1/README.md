# eganalyze

eganalyze is a tool/library for analyzing [Estateguru](https://estateguru.co/) portfolios. It is still very much work in progress, check the open issues to see planned features or to contribute. 

<sub>This tool is not affiliated or endorsed by, or in any way officially connected with Estateguru.</sub>

### What can it do?

At this point the functionality is very limited:

* add column with loan ID (e.g. "EE6452")
* add column with loan URL
* calculate weighted average interest rate

### How do i install it?

```
pip install eganalyze
```

### How do i use it?

1. Change your Estateguru interface to english

2. Go to your [Portfolio Overview](https://estateguru.co/portal/portfolio/details) and download the CSV file

3. Run `eganalyze` on the file:

````console
eganalyze analyze portfolio.csv
````