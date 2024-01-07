# Utilities

## Team contribution analysis via JIRA API.py
This utility traverses all the JIRA issues for a particular sprint, and builds an inverted list of contributors, and how active they were during the reported sprint. The utility saves all the issues it pulls from JIRA into a local file with a timestamp in its name, for auditing purposes and as a local repository. You can re-run the analysis or build more reporting against those snapshots, later, without spending time and bandwidth on pulling the data from JIRA. When you re-run it, it either gets the data from the desired local file, or connects to JIRA API pulling all the issues for the mentioned Sprint.
The report looks like:

| Name | assignee | author | creator | reporter | No roles played | Total Story Points | Issues | SubTasks |
| ---- | -------- | ------ | ------- | -------- | --------------- | ------------------ | ------ | -------- |
| Alice.Johnson@my_domain.com | 1 | 57 | 6 | 6 | | <span style="color:green;font-weight:bold">7</span> | <span style="color:green;font-weight:bold">ABC-723 (14.0/2=7.0)</span> | |
| James.Smith@my_domain.com | 8 | 150 | 13 | 15 | | 133 | ABC-963 (28.0/1=28.0) ABC-805 (105.0/1=105.0) | ABC-1008 (None) ABC-977 (None) |
| Michael.Brown@my_domain.com | 5 | 15 | | | | 98 | ABC-1045 (35.0/1=35.0) ABC-804 (63.0/1=63.0) | ABC-1013 (None) ABC-904 (None) ABC-902 (None) |
| Emma.Wilson@my_domain.com | 13 | 62 | 18 | 18 | | 56 | ABC-1046 (35.0/1=35.0) ABC-657 (21.0/1=21.0) | ABC-1020 (None) ABC-1019 (None) (None) ABC-900 (None) ABC-898 (None) |
| David.Lee@my_domain.com | 2 | 16 | | | | 0 | | ABC-908 (None) ABC-903 (None) |
| John.Davis@my_domain.com | 15 | 80 | 21 | 26 | | <span style="color:green;font-weight:bold">7</span> | <span style="color:green;font-weight:bold">ABC-723 (14.0/2=7.0)</span> | ABC-1030 (None) ABC-1027 (None) ABC-1023 (None) BC-1002 (None)   |
| Olivia.Martin@my_domain.com | | 1 | | | | 0 | | |


## Variety of utilities supporting CICD

ConfigKeyComparer.awk script, v0.2.2, by Slava Luchianov, 5/14/2021
The script compares the config files and finds all the keys which were presented in the sample file and were missed in the secondary files
use it like

**gawk -file ConfigKeyComparer.awk Web.config Web.*.config  > report.log**

Known limitation: the Comparer ignores the config sections, so if the files have the same key name in different sections, the validator considers it as the same key, which might end up with false detection.

What is awk/gawk? It is a powerful scripting engine, and your Windows machine should probably have this AWK engine available somewhere in the git package, in C:\Program Files\Git\usr\bin. Simply include this path into your local variable, and you will have an access to the majority of the Azure CLI/Bash/Unix commands.

ToDo:
Add a Find script for traversing the solution searching for the web.*.config clusters
