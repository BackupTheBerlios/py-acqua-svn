#ifndef _MERGER_H_
#define _MERGER_H_

#include <string>

using namespace std;

class Merger
{
public:
	Merger (const string& filename);
	bool doMerge ();
private:
	void mkDirIfNotPresent (const string& dirname);
	bool eraseAtPath (const string& path, bool is_dir);
	bool updateFile (const string& dirname, const string& filename, const string& md5, long double size);
	string hexDigest (const string& filename);
	
	string m_diff_path;
};

#endif
