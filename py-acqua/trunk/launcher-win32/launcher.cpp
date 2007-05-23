/* This file is part of PyAcqua project
 * Copyright (C) 2001 by Kevin Atkinson under the GNU LGPL license
 * version 2.0 or 2.1.  You should have received a copy of the LGPL
 * license along with this library if you did not you can find
 * it at http://www.gnu.org/.
 */

#include <iostream>
#include <fstream>

using namespace std;

void copy (const string& path1, const string& path2)
{
	ifstream ifs (path1.c_str (), ios::in);
	ofstream ofs (path2.c_str (), ios::out);

	char const_buf[4096];
	
	while (!ifs.eof())
	{
		ifs.read (const_buf, sizeof(const_buf));
		ofs.write (const_buf, ifs.gcount());		
	}

	ifs.close ();
	ofs.close ();
}

int main (int argc, char *argv[])
{
	string orig (argv[1]), dest (argv[2]);
	copy (orig, dest);
	cout << orig << " to " << dest << endl;
}
