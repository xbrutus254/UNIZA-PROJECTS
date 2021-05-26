#pragma once

#include "kriterium_uj_nazov.h"
#include "kriterium_uj_prislusnost.h"
#include "UzemnaJedn.h"
#include "sorted_sequence_table.h"
#include "unsorted_sequence_table.h"
#include "filter_hodnota.h"
#include <string>

using namespace std;
using namespace structures;

class filter_uj_prislusnost : public filter_hodnota<UzemnaJednotka, string>
{
public:
	filter_uj_prislusnost(string nazov_uj);
	UzemnaJednotka* p_uj = nullptr;
	UnsortedSequenceTable<string, UzemnaJednotka*>* filtruj(SortedSequenceTable<string, UzemnaJednotka*>* data) override;
};


// konstruktor
filter_uj_prislusnost::filter_uj_prislusnost(string nazov_uj) : filter_hodnota(nazov_uj, new Kriterium_uj_nazov())
{
}


UnsortedSequenceTable<string, UzemnaJednotka*>* filter_uj_prislusnost::filtruj(SortedSequenceTable<string, UzemnaJednotka*>* data)
{
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
