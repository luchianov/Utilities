BEGIN { 
	print "ConfigKeyComparer awk script, v0.2.2, by Slava Luchianov, 5/14/2021";
	print "use me like gawk -file test.awk Web.config Web.*.config  > report.log";
	if (ARGC < 3 ) {print "insufficient parameters";exit 0;}
	print "Files to process:"
	for(p in ARGV) if (ARGV[p] != "gawk") print ARGV[p];
	print SAMPLE=ARGV[1], " is a SAMPLE file, the rest are the validated files";
}
/add key=".*"/ { keysPerFile[FILENAME][$2] = FILENAME;}
END {
	print "Keys from the ", SAMPLE, " not found in the following files:";
	for (file in keysPerFile) 
	{
		if (file == SAMPLE) continue;
		print "Validating the keys in the ", file;
		for(key in keysPerFile[SAMPLE]) if (keysPerFile[file][key] != file) print "not found: ", key;
	}
}

