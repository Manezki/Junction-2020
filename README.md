# Junction 2020 hackathon
## Visualizing Educational Development Statistics from Opetushallitus

OPH awards millions of euros in grants to different educational projects each year. Currently, it is difficult to keep an overview on how this money is spent and what its impact is. This simple dashboard is a step towards such an overview. It currently focuses on the aspect of spending (which should be relevant to the people at Opetushallitus), but text-mining the grant reports would arguably allow an even more effective summarization of reports.

## Codebase
The dashboard is build with a bit unconventional tooling, by writing HTML from vanilla Python. It served as an interesting lesson on the possibilities and drawbacks of the HTML.

## Data
The data is included with the code, as I see no guarantee it will be available in such a format in the future. Best of my knowledge, there's no limitations for publicing this data, as it should be already publicly available through Opetushallitus.

## Usage
The codebase consists of multiple scripts. Following actions should correctly build the static HTML pages needed for the dashboard.
```
1. python dataSplit.py
2. mkdir categories
3. python indexGenerator.py
4. python categoryGenerator.py
```
