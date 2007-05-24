#include <iostream>
#include <fstream>
#include <string>

#include "merger.h"

using namespace std;

int main (int argc, char *argv[])
{
	
	char *tmp = getenv ("APPDATA");
	
	cout << tmp << endl;
	string path (tmp);
	
	path += "\\.pyacqua\\update\\.diff.xml";
	
	cout << "Path: " << path << endl;
	
	Merger merger (path);
	
	if (!merger.doMerge ())
		return -1;

	system ("pause");
	return 0;
}
