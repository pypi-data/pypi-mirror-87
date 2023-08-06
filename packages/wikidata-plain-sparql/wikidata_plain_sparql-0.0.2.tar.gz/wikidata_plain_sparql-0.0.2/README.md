# WikiData Plain SPARQL Client
This package allows to query the WikiData database. For example this package is intended for people who need to be able to query WikiData in plain SPARQL while staying whithin a Jupyter Notebook.

## Install
```bash
pip install wikidata_plain_sparql
```

## Usage
The module only has one function which is named query:
```python
# import the module
import wikidata_plain_sparql as wikidata

# query WikiData
wikidata.query('''
SELECT ?actor ?actorLabel
WHERE
{
  # Person of Interest has actor
  wd:Q564345 wdt:P161 ?actor.
  # actor has won a Golden Globe Award
  ?actor wdt:P166 wd:Q1011547.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
''')
```
Which will result in the following pandas data frame:
| actor | actorLabel |
| --- | --- |
| http://www.wikidata.org/entity/Q3295000 | Sterling K. Brown |

## Credits
- [@jelleschutter](https://github.com/jelleschutter/) - Development