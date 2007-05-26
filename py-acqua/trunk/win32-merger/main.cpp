#include <iostream>
#include <fstream>
#include <string>
#include <windows.h>

#include "merger.h"

using namespace std;

void start (const char *path)
{
	STARTUPINFO si;
	PROCESS_INFORMATION pi;
	
	ZeroMemory (&si, sizeof (si));
	si.cb = sizeof (si);
	ZeroMemory (&pi, sizeof (pi));
	
	CreateProcess (
	    path,
	    NULL,
	    NULL,
		NULL,
		FALSE,
		0,
		NULL,
		NULL,
		&si,
		&pi
	);
	
	//WaitForSingleObject (pi.hProcess, INFINITE);
	
	CloseHandle (pi.hProcess);
	CloseHandle (pi.hThread);
}
#if 0
int main (int argc, char *argv[])
#else
int STDCALL
WinMain (HINSTANCE hInstance, HINSTANCE hPrev, LPSTR lpCmd, int nShow)
#endif
{
	Merger merger;
	merger.doMerge ();

	/* Create Process */
	start ("acqua.exe");
	
	return 0;
}
