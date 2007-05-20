/* This file is part of PyAcqua project
 * Copyright (C) 2001 by Kevin Atkinson under the GNU LGPL license
 * version 2.0 or 2.1.  You should have received a copy of the LGPL
 * license along with this library if you did not you can find
 * it at http://www.gnu.org/.
 */

#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <fstream>

#define MERGER "merger.exe"
#define PYACQUA "acqua.exe"

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


void start (char *program, bool console)
{
	STARTUPINFO si;
	PROCESS_INFORMATION pi;

	ZeroMemory (&si, sizeof (si));
	si.cb = sizeof (si);
	ZeroMemory (&pi, sizeof (pi));

	if (!CreateProcess(console ? NULL : program, console ? program : NULL, NULL, NULL, console ? TRUE : FALSE, console ? CREATE_NEW_CONSOLE : 0, NULL, NULL, &si, &pi)) 
		return;
	
	WaitForSingleObject (pi.hProcess, INFINITE);

	CloseHandle (pi.hProcess);
	CloseHandle (pi.hThread);
}
#if 0
int STDCALL
WinMain (HINSTANCE hInst, HINSTANCE hPrev, LPSTR lpCmd, int nShow)
#endif
int main ()
{
	char *app_data = getenv("APPDATA");
	
	string path (app_data);
	path += "\\.pyacqua\\update\\.diff.xml";
	
	cout << "checking " << path << endl;

	fstream test_file;
	test_file.open (path.c_str (), ios::in);
	
	if (test_file.good ())
	{
                        cout << "ok" << endl;
		char cur_dir[MAX_PATH];
		
		if (GetCurrentDirectory (MAX_PATH, cur_dir) == 0)
		   return 0;
		
		string path1 (cur_dir);
		path1 += "\\" MERGER;
		
		string path2 (cur_dir);
		path2 = path2.substr (0, path2.length () - 7);
		path2 += MERGER;
		
		copy (path1, path2);
		
		cout << "file copied " << path1 << " to " << path2 << endl;
		
		start (strdup (path2.c_str ()), true);
		
		::remove (path2.c_str ());
	}
	
	start (PYACQUA, false);
	
	system ("pause");
	return 0;
}
