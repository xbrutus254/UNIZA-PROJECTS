#pragma once

#include "Kriterium.h"
#include "sorted_sequence_table.h"
#include "unsorted_sequence_table.h"

using namespace std;
using namespace structures;

template<typename K, typename T>
class Filter {
public:
	Kriterium<K, T>* kriterium;
	Filter(Kriterium<K, T>* p_kriterium);
	virtual ~Filter();

	virtual bool splnaFilter(K* o) = 0;
	//virtual UnsortedSequenceTable<string, O*>* filtrujNeutriedena(SortedSequenceTable<string, O*>* tabulka) = 0;
	//virtual SortedSequenceTable<string, O*>* filtrujUtriedena(SortedSequenceTable<string, O*>* tabulka) = 0;

	virtual UnsortedSequenceTable<string, UzemnaJednotka*>* filtruj(SortedSequenceTable<string, K*>* data) = 0;

	

};

template<typename K, typename T>
inline Filter<K, T>::Filter(Kriterium<K, T>* p_k)
{
	kriterium = p_k;
}

template<typename K, typename T>
inline Filter<K, T>::~Filter()
{
	delete kriterium;
}