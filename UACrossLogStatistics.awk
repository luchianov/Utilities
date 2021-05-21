BEGIN { 
	print "UA Cross Log Statistics awk script, v0.1.0, by Slava Luchianov, 5/21/2021";
	print "use me like gawk -file UACrossLogStatistics.awk DavitaUserAutomationLog_*.log";
	print "Files to process:"
	for(p in ARGV) if (ARGV[p] != "gawk") printf " ", ARGV[p];
	print "\n"
}
/15:27:14  - Start time: 5/21/2021 3:27:14 PM/ {
	keysPerFile[FILENAME] = $0
}
END {
	print "Keys from the Files";
	for (file in keysPerFile) 
	{
		print "File <", file, "> \nContent captured";
		for(row in keysPerFile[file]) print "not found: ", row;
	}
}

