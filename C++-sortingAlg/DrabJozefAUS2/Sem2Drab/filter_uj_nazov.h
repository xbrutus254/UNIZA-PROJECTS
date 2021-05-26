#pragma once

#include "kriterium_uj_nazov.h"
#include "UzemnaJedn.h"
#include "sorted_sequence_table.h"
#include "unsorted_sequence_table.h"
#include "filter_hodnota.h"
#include <string>

using namespace std;
using namespace structures;

class filter_uj_nazov : public filter_hodnota<UzemnaJednotka, string>
{
public:
	filter_uj_nazov(string nazov_uj);

	UnsortedSequenceTable<string, UzemnaJednotka*>* filtruj(SortedSequenceTable<string, UzemnaJednotka*>* data) override;
private:
	string nazov_uj_at;
};


// konstruktor
filter_uj_nazov::filter_uj_nazov(string nazov_uj) : filter_hodnota(nazov_uj, new Kriterium_uj_nazov())
{
	nazov_uj_at = nazov_uj;
}


UnsortedSequenceTable<string, UzemnaJednotka*>* filter_uj_nazov::filtruj(SortedSequenceTable<string, UzemnaJednotka*>* data)
{
	UnsortedSequenceTable<string, UzemnaJednotka*>* tabulka = new UnsortedSequenceTable<string, UzemnaJednotka*>();
	/*for (auto prvok : *data)	// pre kazdu UJ rob
	{
		if (splnaFilter(prvok->accessData()))	// ak nazov sedi
		{
			if (!tabulka->containsKey(prvok->getKey())) // ak v tabulke este nie je tkay prvok
			{
				tabulka->insert(prvok->getKey(), prvok->accessData());	// vloz ho
			}
		}
	}*/ //NEVHODNE KEDZE TATO OPERACIA MA ZLOZITOST O(N)
	int begin = 0;
	int end = data->size()-1;
	
	int pointer = (end + begin) / 2;
	
	//auto prvok = tabulka->getItemAtIndex(pointer);
	//cout << prvok.getKey() << endl;
	while (1) {								// TATO ZLOZITOST JE O(LOG n )
		//cout << "pointer: " << pointer << endl;
		auto prvok = data->getItemAtIndex(pointer);
		if (splnaFilter(prvok.accessData()))
		{
			tabulka->insert(prvok.getKey(), prvok.accessData());
			break;
		}
		else {
			//cout << prvok.getKey() << " ? " << nazov_uj_at << endl;
			if (prvok.getKey() > nazov_uj_at) {
				end = pointer;
				pointer = (end + begin) / 2;
			}
			else if (prvok.getKey() < nazov_uj_at) {
				begin = pointer;
				pointer = (end + begin) / 2;
			}
		}

	}

	return tabulka;
}
