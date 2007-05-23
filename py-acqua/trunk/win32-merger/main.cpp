#include <iostream>
#include <fstream>
#include <string>
#include "md5.h"

using namespace std;

/**
 * Produce un hexdigest MD5 come stringa
 * @param filename il percorso del file di cui calcolare il checksum
 * @return l'hexdigest md5 come std::string
 */
string hexdigest (const char *filename)
{
	md5_state_t context;
	MD5 hasher;

	unsigned char buff[1024], digest[16];

	ifstream file;
	file.open (filename, ios::in);

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

int main (int argc, char *argv[])
{
	if (argc != 2)
		return -1;

	cout << hexdigest (argv[1]) << endl;

	return 0;
}
