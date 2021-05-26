#pragma once
#include "Filter.h"
#include "Kriterium.h"

using namespace std;
using namespace structures;

template<typename K, typename T>
class filter_hodnota : public Filter<K, T>
{
public:
	filter_hodnota(T hodnota, Kriterium<K, T>* param_kriterium);
	~filter_hodnota() {};
	bool splnaFilter(K* o) override;

	virtual UnsortedSequenceTable<T, UzemnaJednotka*>* filtruj(SortedSequenceTable<string, K*>* data) = 0;

private:
	T hodnota;
};

template<typename K, typename T>
inline filter_hodnota<K, T>::filter_hodnota(T param_hodnota, Kriterium<K, T>* param_kriterium) : Filter<K, T>::Filter(param_kriterium)
{

	hodnota = param_hodnota;
}

template<typename K, typename T>
inline bool filter_hodnota<K, T>::splnaFilter(K* o)
{
	if (hodnota != Filter<K, T>::kriterium->ohodnot(o)) {
		//cout << "bolo false" << endl;
		return false;
	}
	else {
		//cout << "bolo true" << endl;
		return true;
	}

}