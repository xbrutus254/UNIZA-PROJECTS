#pragma once

#include "kriterium_zastavanost.h"
#include "UzemnaJedn.h"
#include "sorted_sequence_table.h"
#include "unsorted_sequence_table.h"
#include "filter_interval.h"
#include <string>

using namespace std;
using namespace structures;

class filter_zastavanost : public filter_interval<UzemnaJednotka, long long>
{
public:
	filter_zastavanost(long long p_min, long long p_max);

	UnsortedSequenceTable<string, UzemnaJednotka*>* filtruj(SortedSequenceTable<string, UzemnaJednotka*>* data) override;
};


// konstruktor

filter_zastavanost::filter_zastavanost(long long p_min, long long p_max) : filter_interval(new Kriterium_zastavanost(), p_min, p_max)
{
}


UnsortedSequenceTable<string, UzemnaJednotka*>* filter_zastavanost::filtruj(SortedSequenceTable<string, UzemnaJednotka*>* data) {
	UnsortedSequenceTable<string, UzemnaJednotka*>* tabulka = new UnsortedSequenceTable<string, UzemnaJednotka*>();
	for (auto prvok : *data)
	{
		if (splnaFilter(prvok->accessData()))
		{
			if (!tabulka->containsKey(prvok->getKey()))
			{
				tabulka->insert(prvok->getKey(), prvok->accessData());
			}
		}
	}
	return tabulka;
}
