#ifndef _MERGER_H_
#define _MERGER_H_

#include <string>

using namespace std;

class Merger
{
public:
	Merger ();
	bool doMerge ();
	
private:
	void mkDirIfNotPresent (const string& dirname);
	bool eraseAtPath (const string& path, bool is_dir);
	bool updateFile (const string& dirname, const string& filename, const string& md5, long long size);

	string hexDigest (const string& filename);
	bool copyFile (const string& orig, const string& dest, bool remove_orig);
	void deleteDirectory (const char *dir);
	
	string m_diff_path;
	string m_update_dir;
};

#endif
