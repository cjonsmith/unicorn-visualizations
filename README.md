# Unicorn Visualizations

A set of several simple Python scripts to perform data analysis and
visualization on the current "[unicorn
companies](https://en.wikipedia.org/wiki/Unicorn_(finance))"

## Contents

### scrape.py

The web scraping script. Uses the
[requests](http://docs.python-requests.org/en/master/) module and
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) to retrieve and
parse the data from the website: [https://www.cbinsights.com/research-unicorn-companies](https://www.cbinsights.com/research-unicorn-companies).

The data from the table on the webpage will be saved as a 
[pandas](http://pandas.pydata.org/) DataFrame object, which will then be
serialized as "frame.p" using the builtin
[pickle]("https://docs.python.org/3/library/pickle.html") module.

In order to use the data collected, the script must be executed to generate the
serialized DataFrame.

### plot.py

_Work in progress._

Currently prints the investor who has invested in the most unicorn companies.
