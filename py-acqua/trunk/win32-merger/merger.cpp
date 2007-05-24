#include "merger.h"

#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <windows.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <direct.h>

#include "tinyxml/tinyxml.h"
#include "md5.h"

#define MAXPATH 2048

Merger::Merger (const string& filename) : m_diff_path (filename)
{
}

bool Merger::doMerge ()
{
    TiXmlDocument doc (m_diff_path.c_str ());
    
	if (!doc.LoadFile ())
	    return false;
	
    TiXmlHandle hDoc (&doc);
    TiXmlElement *pElem, *pChildElem;
    TiXmlHandle hRoot(0);

    pElem = hDoc.FirstChildElement ().Element ();

    if (!pElem || pElem->ValueStr () != "pyacqua")
        return false;

	hRoot = TiXmlHandle (pElem);
	pElem = hRoot.FirstChild ().Element ();

	for (pElem; pElem; pElem = pElem->NextSiblingElement ())
	{
        bool to_delete = false;

		if (pElem->ValueStr () != "directory")
		    continue;

		string dirname = pElem->Attribute ("name");

		if (dirname.substr (0, 2) == "$$" &&
			dirname.substr (dirname.length () - 2) == "$$")
			to_delete = true;

		hRoot = TiXmlHandle (pElem);
		pChildElem = hRoot.FirstChild ().Element ();

		if (to_delete)
			dirname = dirname.substr (2, dirname.length () - 4);
		else
		    mkDirIfNotPresent (dirname);

		for (pChildElem; pChildElem; pChildElem = pChildElem->NextSiblingElement ())
		{
			if (pChildElem->ValueStr () != "file")
				continue;

			long double size = -1;
			string md5 = pChildElem->Attribute ("md5");
			string filename = pChildElem->Attribute ("name");
			pChildElem->Attribute ("bytes", (double*)&size);

			if (to_delete)
			    eraseAtPath (dirname + "\\" + filename, false);
			else
				updateFile (dirname, filename, md5, size);
		}

		if (to_delete)
		    eraseAtPath (dirname, true);
	}
	
	return true;
}

void Merger::mkDirIfNotPresent (const string& dirname)
{
	cout << "Checking if dir is present " << dirname << endl;

	struct _stat dir_stat;
	
	if (!::_stat (dirname.c_str (), &dir_stat))
	{
		// controlla se e' una dir
		if (S_ISDIR (dir_stat.st_mode))
			return;

		cout << "Is not a dir !" << endl;
	}
	else
		::mkdir (dirname.c_str ());
}

bool Merger::eraseAtPath (const string& path, bool is_dir)
{
    if (!is_dir)
	{
		cout << "Removing " << path << endl;
		::remove (path.c_str ());
		return false;
	}
	else
	{
    	char newsub[MAXPATH];
		char newdir[MAXPATH];
		char fname[MAXPATH];
	
		HANDLE hList;
		
		TCHAR szDir[MAXPATH];
		WIN32_FIND_DATA FileData;
		
		string dirpath (path);
		dirpath += "\\*";
		hList = FindFirstFile (szDir, &FileData);
		
		if (hList == INVALID_HANDLE_VALUE)
		    return false;

		do {
			strncpy (fname, FileData.cFileName, MAXPATH);

			if (!strcmp (fname,".") || !strcmp (fname,".."))
				continue;
			else
			    return false;
		} while (FindNextFile (hList, &FileData));
		
		FindClose (hList);
		
		cout << "No files" << endl;
		::remove (path.c_str ());
		
		return true;
	}
}

bool Merger::updateFile (const string& dirname, const string& filename, const string& md5, long double size)
{
	string path (dirname);
	path += "\\" + filename;
	
	string new_md5 = hexDigest (filename);
	long double new_size = -1;

	struct _stat filestat;
	if (!::_stat (filename.c_str (), &filestat))
	{
		size = filestat.st_size;
	}
	
	if (new_size == size && new_md5 == md5)
	    cout << "OK. Files are the same" << endl;
}

string Merger::hexDigest (const string& filename)
{
    md5_state_t context;
	MD5 hasher;

	unsigned char buff[1024], digest[16];

	ifstream file;
	file.open (filename.c_str (), ios::in);

	if (!file.good ())
		return "";

	hasher.Init (&context);

	while (file.good ())
	{
		file.read ((char *)buff, 1024);
		hasher.Append (&context, buff, file.gcount ());
	}

	hasher.Finish (digest, &context);

	file.close ();

	char temp[32];

	int p = 0;
	for (int i = 0; i < 16; i++)
	{
		::sprintf (&temp[p], "%02x", digest[i]);
		p += 2;
	}

	return string (temp);
}
