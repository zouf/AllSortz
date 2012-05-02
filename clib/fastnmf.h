#ifndef FASTNMF_H
#define FASTNMF_H

#include <vector>

using namespace std;


struct rating_t
{
	int uid;
	int bid;
	uint8_t rat;
};



void run_nmf_from_c(vector<rating_t>  ratings, int N, int M, int K);
void run_nmf_c();

#endif
