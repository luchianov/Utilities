BEGIN { 
	if (ARGC <2 )
	{
		print "UA Cross Log Statistics awk script, v0.1.0, by Slava Luchianov, 5/21/2021";
		print "use me like gawk -file UACrossLogStatistics.awk DavitaUserAutomationLog_*.log";
		print "Files to process:";
		for(p in ARGV) if (ARGV[p] != "gawk") printf " ", ARGV[p];
		print "\n";
	}
}
#/.*/{
/[0-9]+:[0-9]+:[0-9]+  - Start time: [0-9]+\/[0-9]+\/[0-9]+.*$/{
	keysPerFile[FILENAME][1] = $5;
	keysPerFile[FILENAME][2] = $1;
	keysPerFile[FILENAME][3] = \
	keysPerFile[FILENAME][4] = \
	keysPerFile[FILENAME][5] = \
	keysPerFile[FILENAME][6] = \
	keysPerFile[FILENAME][7] = \
	keysPerFile[FILENAME][8] = \
	keysPerFile[FILENAME][9] = \
	keysPerFile[FILENAME][10] = \
	keysPerFile[FILENAME][11] = "";
	# keysPerFile[FILENAME][12] = FILENAME;
}
/[0-9]+:[0-9]+:[0-9]+  -  User Automation Process has completed sucessfully/ {
	keysPerFile[FILENAME][3] = $1;
}
/[0-9]+:[0-9]+:[0-9]+  - [0-9]+ upcoming user... have changes in location/ {
	keysPerFile[FILENAME][4] = $3;
}
/[0-9]+:[0-9]+:[0-9]+  - Updating locations for [0-9]+ users/ {
	keysPerFile[FILENAME][5] = $6;
}
/[0-9]+:[0-9]+:[0-9]+  - Hierarchy Nodes to re-activate: [0-9]+/ {
	keysPerFile[FILENAME][6] = $7;
}
/[0-9]+:[0-9]+:[0-9]+  - Hierarchy Nodes to deactivate: [0-9]+/ {
	keysPerFile[FILENAME][7] = $7;
}
/[0-9]+:[0-9]+:[0-9]+  - Locations to reactivate: [0-9]+/ {
	keysPerFile[FILENAME][8] = $6;
}
/[0-9]+:[0-9]+:[0-9]+  - Locations to deactivate: [0-9]+/ {
	keysPerFile[FILENAME][9] = $6;
}
/[0-9]+:[0-9]+:[0-9]+  - Location Access to reactivate: [0-9]+/ {
	keysPerFile[FILENAME][10] = $7;
}
/[0-9]+:[0-9]+:[0-9]+  - Location Access to deactivate: [0-9]+/ {
	keysPerFile[FILENAME][11] = $7;
}
END {
	print "StartDate, StartTime, StopTime, UserAffectedByLocReg, UpdatingUserLocReg, NodesReactivate, NodesDeactivate, LocReactivate, LocDeactivate, AccessReactivate, AccessDeactivate, File";
	for (file in keysPerFile) 
	{
		# for(row in keysPerFile[file]) printf row "-" keysPerFile[file][row] ", ";
		for(row in keysPerFile[file]) printf keysPerFile[file][row] ", ";
		printf "\n";
	}
}

