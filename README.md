# Utilities

## Team contribution analysis via JIRO API.py
This utility traverses all the JIRA issues for a particular sprint, and builds an inverted list of contributors, and how active they were during the reported sprint.
The utility saves all the issues it pulls from JIRA into a local file with a timestamp in its name, for auditing purposes and as a local repository. 
You can re-run the analysis or build more reporting against those snapshots, later, without spending time and bandwidth on pulling the data from JIRA.

## Variety of utilities supporting CICD

ConfigKeyComparer.awk script, v0.2.2, by Slava Luchianov, 5/14/2021
The script compares the config files and finds all the keys which were presented in the sample file and were missed in the secondary files
use it like

**gawk -file ConfigKeyComparer.awk Web.config Web.*.config  > report.log**

Known limitation: the Comparer ignores the config sections, so if the files have the same key name in different sections, the validator considers it as the same key, which might end up with false detection.

What is awk/gawk? It is a powerful scripting engine, and your Windows machine should probably have this AWK engine available somewhere in the git package, in C:\Program Files\Git\usr\bin. Simply include this path into your local variable, and you will have an access to the majority of the Azure CLI/Bash/Unix commands.

ToDo:
Add a Find script for traversing the solution searching for the web.*.config clusters
