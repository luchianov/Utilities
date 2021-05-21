"C:\Program Files\Git\usr\bin\find.exe" C:\Dev\Integrations\integrations_development\fmPilot.API\fmPilot.API.Client -iname "web.config" -printf 'cd %%h\ngawk -f C:/Users/vluchiano/Documents/GitRepos/ConfigKeyComparer.awk web.config web.*.config \n'

C:\Users\vluchiano\documents\gitrepos>"C:\Program Files\Git\usr\bin\find.exe" C:\Dev\Integrations\integrations_development\fmPilot.API\fmPilot.API.Client -iname "web.config" -printf 'cd %h\ngawk -f C:/Users/vluchiano/Documents/GitRepos/ConfigKeyComparer.awk web.config web.*.config \n' 

cd C:\Dev\Integrations\integrations_development\fmPilot.API\fmPilot.API.Client/Areas/HelpPage/Views

gawk -f C:/Users/vluchiano/Documents/GitRepos/ConfigKeyComparer.awk web.config web.*.config 
