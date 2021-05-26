#pragma once

#include "kriterium_pocet_obyv.h"
#include "UzemnaJedn.h"
#include "sorted_sequence_table.h"
#include "unsorted_sequence_table.h"
#include "filter_interval.h"
#include <string>

using namespace std;
using namespace structures;

class filter_obyvatelia : public filter_interval<UzemnaJednotka, int>
{
public:
	filter_obyvatelia(int p_min, int p_max);

	UnsortedSequenceTable<string, UzemnaJednotka*>* filtruj(SortedSequenceTable<string, UzemnaJednotka*>* data) override;
};


// konstruktor

filter_obyvatelia::filter_obyvatelia(int p_min, int p_max) : filter_interval(new Kriterium_pocet_obyv(), p_min, p_max)
{
}


UnsortedSequenceTable<string, UzemnaJednotka*>* filter_obyvatelia::filtruj(SortedSequenceTable<string, UzemnaJednotka*>* data) {
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
