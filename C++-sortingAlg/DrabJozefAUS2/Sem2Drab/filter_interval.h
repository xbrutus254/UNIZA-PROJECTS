#pragma once
#include "Filter.h"
#include "Kriterium.h"

using namespace std;
using namespace structures;

template<typename K, typename T>
class filter_interval : public Filter<K, T>
{
public:
	filter_interval(Kriterium<K, T>* param_kriterium, long long p_min, long long p_max);
	~filter_interval() {};
	bool splnaFilter(K* o) override;

	virtual UnsortedSequenceTable<string, UzemnaJednotka*>* filtruj(SortedSequenceTable<string, K*>* data) = 0;

private:
	T dolna_h;
	T horna_h;
};

template<typename K, typename T>
inline filter_interval<K, T>::filter_interval(Kriterium<K, T>* param_kriterium, long long p_min, long long p_max) : Filter<K, T>::Filter(param_kriterium)
{
	// TODOOOO
	dolna_h = p_min;
	horna_h = p_max;
}

template<typename K, typename T>
inline bool filter_interval<K, T>::splnaFilter(K* o)
{
	//I aktualny = Filter<K, T>::kriterium->ohodnot(o);
	
	if (dolna_h <= Filter<K, T>::kriterium->ohodnot(o) && Filter<K, T>::kriterium->ohodnot(o) <= horna_h) {
	//if (dolna_h <= Filter<K, T>::kriterium->ohodnot(o)) {
		//cout << "dolna_h: " << <int>dolna_h << "aktual: " << <int>aktualny << "horna_h: " << <int>horna_h << end;
		return true;
	}
	else {
		return false;
	}

}