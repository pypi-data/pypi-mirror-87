# 📈 eganalyze

eganalyze is a tool/library for analyzing [Estateguru](https://estateguru.co/) portfolios. It is still very much work in progress, check the open issues to see planned features or to contribute. 

<sub>This tool is not affiliated or endorsed by, or in any way officially connected with Estateguru.</sub>

### What can it do?

At this point the functionality is very limited. Currently it can

* Enrich the CSV with
    * normalize column names
    * add column with loan ID (e.g. "EE6452")
    * add column with loan URL

* Calculate the following key performance indicators
    * mean ltv
    * outstanding mean ltv
    * outstanding weighted mean ltv
    * mean interest rate
    * outstanding mean interest rate
    * outstanding weighted mean interest rate     

### How do i install it?

```
pip install eganalyze
```

### How do i use it?

1. Change your Estateguru interface to english

2. Go to your [Portfolio Overview](https://estateguru.co/portal/portfolio/details) and download the CSV file

3. Run `eganalyze` on the file to print key performance indicators:

```console
$ eganalyze analyze portfolio.csv
Mean interest rate: 11.04%
Outstanding mean interest rate: 10.79%
Outstanding weighted mean interest rate: 10.75%
Mean LTV: 54.23%
Outstanding mean LTV: 54.35%
Outstanding weighted mean LTV: 54.11%
```

### Advanced usage


```console
$ eganalyze --help
Usage: eganalyze [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  analyze  Analyze given portfolio and print key performance indicators
  process  Normalize, enrich, process CSV and output to file
```
