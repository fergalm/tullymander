#%% markdown
"""
# Tullymander

This tool simulates the results of different elections for Baltimore County Council districts, had the districts been drawn differently. By moving precincts between districts, you can see how different candidates would have performed in those districts as their boundaries changes.

## To start
Select the block of code below and hit [SHIFT] + [ENTER]. This will cause a plot, and a table to appear. The table shows the population of each district and the net vote share for a range of candidates in recent elections (net vote share is the difference between the number of votes for the candidate, and the number for the most popular opponent).

Move your mouse over a precinct and type the number of the district you want that precinct to be moved to. For example, point your mouse at one of the precincts in the extreme north of the county, and assign them to district 7 by hitting the [7] key. The precinct will change colour, and the table with update to show the population and vote shares of the newly drawn districts 3 and 7.
"""
#%% code
%matplotlib notebook
from IPython.display import display
import ipywidgets
import iface

console = ipywidgets.Output()
configfile = "../config/council.toml"
widgets = iface.setup(configfile, console)
display(*widgets)