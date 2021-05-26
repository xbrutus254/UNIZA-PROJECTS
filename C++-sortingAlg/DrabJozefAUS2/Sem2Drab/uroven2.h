#pragma once
#include "sorted_sequence_table.h"
#include "unsorted_sequence_table.h"

#include "Stat.h"
#include "quick_sort.h"

#include "kriterium_uj_nazov.h"
#include "kriterium_uj_typ.h"
#include "kriterium_uj_prislusnost.h"
#include "Kriterium_pocet_obyv.h"
#include "Kriterium_predpro.h"
#include "Kriterium_pro.h"
#include "Kriterium_popro.h"
#include "Kriterium_celkovaVymera.h"
#include "Kriterium_zastavanost.h"
#include "Kriterium_zastavPlocha.h"

#include "filter_uj_nazov.h"
#include "filter_obyvatelia.h"
#include "filter_interval.h"
#include "filter_zastavanost.h"


#include <iostream>
#include <fstream>
#include <string>
//#include <atlbase.h>




using namespace std;

class uroven2
{
public:
	uroven2(Stat* param_data);
	~uroven2() {};

	
private:
	Stat* stat_data = nullptr;
	SortedSequenceTable<string, UzemnaJednotka*>* tabulka;
	
	template<typename T, typename K>
	UnsortedSequenceTable<T, UzemnaJednotka*>* zorad(Kriterium_uzemnej_j<T>& p_krit, SortedSequenceTable<string, K>& tabulka, bool zostupne);

	void spust();
	bool obec = false;
	bool okres = false;
	bool kraj_f = false;
	bool okres_f = false;
	string nazov_kraja = "";
	string nazov_okresu = "";
};




template<typename T, typename K>
inline UnsortedSequenceTable<T, UzemnaJednotka*>* uroven2::zorad(Kriterium_uzemnej_j<T>& p_krit, SortedSequenceTable<string, K>& tabulka, bool zostupne)
{
	Kriterium_uzemnej_j<T>* kriterium = &p_krit;
	UnsortedSequenceTable<T, UzemnaJednotka*>* com_table = new UnsortedSequenceTable<T, UzemnaJednotka*>();

	/*for (auto l : tabulka) {
		if (l->accessData()->containsKey(kriterium->ohodnot(l->accessData())))
		{
			com_table->insert(l->accessData());
		}
	}
	return com_table;*/
	for (auto prvok : tabulka)
	{
		T kluc = kriterium->ohodnot(prvok->accessData());
		if (!com_table->containsKey(kluc))
		{
			com_table->insert(kluc, prvok->accessData());
		}
	}
	return com_table;
}

uroven2::uroven2(Stat* param_data)
{
	stat_data = param_data;
	int vyber = 4;
	cout << endl << "Zadaj co chces testovat:" << endl;
	cout << "(1.) Kraje" << endl;
	cout << "(2.) Okresy" << endl;
	cout << "(3.) Obce" << endl;
	cin >> vyber;

	if (vyber == 1)
	{
		tabulka = stat_data->get_kraje();
		obec = false;
		okres = false;
		spust();
	}
	else if (vyber == 2)
	{
		tabulka = stat_data->get_okresy();
		obec = false;
		okres = true;
		spust();
	}
	else if (vyber == 3)
	{
		tabulka = stat_data->get_obce();
		obec = true;
		okres = true;
		spust();
	}
	else {
		cout << "Zadal si nespravne cislo" << endl;
	}
}

void uroven2::spust() {

	std::cout << endl << "Chces pouzit filter prislusnost?" << endl;
	std::cout << "(1.) ano" << endl;
	std::cout << "(2.) nie." << endl;
	int vyber;
	std::cin >> vyber;

	if (vyber == 1) {
		if (obec && okres) {
			std::cout << endl << "Podla ktorej prislusnej jednotky chces filtrovat?" << endl;
			std::cout << "(1.) kraj" << endl;
			std::cout << "(2.) okres" << endl;
			std::cin >> vyber;
			if (vyber == 1)
			{
				kraj_f = true;
				okres_f = false;
				std::cout << endl << "Zadaj nazov kraja: " << endl;
				while (nazov_kraja == "")
					std::getline(std::cin, nazov_kraja);
			}
			else if (vyber == 2)
			{
				kraj_f = false;
				okres_f = true;
				std::cout << endl << "Zadaj nazov okresu: " << endl;
				while (nazov_okresu == "")
					std::getline(std::cin, nazov_okresu);
			}
		}
		else if (!obec && okres) {
			std::cout << endl << "Zadaj nazov kraja: " << endl;
			while (nazov_kraja == "")
			{
				std::getline(std::cin, nazov_kraja);
			}
		}
	}


	Kriterium_uj_nazov* kriterium_nazov = new Kriterium_uj_nazov();
	Kriterium_pocet_obyv* kriterium_po = new Kriterium_pocet_obyv();
	Kriterium_zastavanost* kriterium_zast = new Kriterium_zastavanost();
	vyber = 5;

	while (1) {
		cout << endl << "Zadaj ktoru ulohu chces robit:" << endl;
		cout << "(1.) Zorad podla nazvu" << endl;
		cout << "(2.) Zorad podla poctu obyv." << endl;
		cout << "(3.) Zorad podla zastavanosti" << endl;

		cin >> vyber;
		if (vyber == 1) {

			UnsortedSequenceTable<string, UzemnaJednotka*>* zoradena_tab = uroven2::zorad(*kriterium_nazov, *tabulka, true);
			QuickSort<string, UzemnaJednotka*>* q = new QuickSort<string, UzemnaJednotka*>();

			cout << "(0.) Vzostupne" << endl;
			cout << "(1.) Zostupne" << endl;
			cin >> vyber;

			if (vyber == 0) {
				q->sort(*zoradena_tab);
			}
			else if (vyber == 1) {
				q->sort_r(*zoradena_tab);
			}

			for (auto item : *zoradena_tab) {
				if (nazov_kraja != "")
				{
					if (obec && okres) {
						if (item->accessData()->get_parent()->get_parent()->get_nazov_uj() != nazov_kraja)
							continue;
					}
					else {
						if (item->accessData()->get_parent()->get_nazov_uj() != nazov_kraja)
							continue;
					}
					
				}
				else if (nazov_okresu != "")
				{
					if (item->accessData()->get_parent()->get_nazov_uj() != nazov_okresu)
						continue;
				}
				cout << Kriterium_uj_nazov().ohodnot(item->accessData()) << endl;
			}
			delete q;
			delete zoradena_tab;
		}
		else if (vyber == 2) {

			UnsortedSequenceTable<int, UzemnaJednotka*>* zoradena_tab = uroven2::zorad(*kriterium_po, *tabulka, true);
			QuickSort<int, UzemnaJednotka*>* q = new QuickSort<int, UzemnaJednotka*>();

			cout << "(0.) Vzostupne" << endl;
			cout << "(1.) Zostupne" << endl;
			cin >> vyber;

			if (vyber == 0) {
				q->sort(*zoradena_tab);
			}
			else if (vyber == 1) {
				q->sort_r(*zoradena_tab);
			}

			for (auto item : *zoradena_tab) {
				if (nazov_kraja != "")
				{
					if (obec && okres) {
						if (item->accessData()->get_parent()->get_parent()->get_nazov_uj() != nazov_kraja)
							continue;
					}
					else {
						if (item->accessData()->get_parent()->get_nazov_uj() != nazov_kraja)
							continue;
					}

				}
				else if (nazov_okresu != "")
				{
					if (item->accessData()->get_parent()->get_nazov_uj() != nazov_okresu)
						continue;
				}
				//cout << Kriterium_uj_nazov().ohodnot(item->accessData()) << endl;
				cout << Kriterium_uj_nazov().ohodnot(item->accessData()) << " | pocet obyv: " << Kriterium_pocet_obyv().ohodnot(item->accessData()) << endl;
			}
			delete q;
			delete zoradena_tab;
		}
		else if (vyber == 3) {

			UnsortedSequenceTable<long long, UzemnaJednotka*>* zoradena_tab = uroven2::zorad(*kriterium_zast, *tabulka, true);
			QuickSort<long long, UzemnaJednotka*>* q = new QuickSort<long long, UzemnaJednotka*>();

			cout << "(0.) Vzostupne" << endl;
			cout << "(1.) Zostupne" << endl;
			cin >> vyber;

			if (vyber == 0) {
				q->sort(*zoradena_tab);
			}
			else if (vyber == 1) {
				q->sort_r(*zoradena_tab);
			}

			for (auto item : *zoradena_tab) {
				if (nazov_kraja != "")
				{
					if (obec && okres) {
						if (item->accessData()->get_parent()->get_parent()->get_nazov_uj() != nazov_kraja)
							continue;
					}
					else {
						if (item->accessData()->get_parent()->get_nazov_uj() != nazov_kraja)
							continue;
					}

				}
				else if (nazov_okresu != "")
				{
					if (item->accessData()->get_parent()->get_nazov_uj() != nazov_okresu)
						continue;
				}
				//cout << Kriterium_uj_nazov().ohodnot(item->accessData()) << endl;
				cout << Kriterium_uj_nazov().ohodnot(item->accessData()) << " | pocet obyv: " << Kriterium_zastavanost().ohodnot(item->accessData()) << endl;
			}
			delete q;
			delete zoradena_tab;
		}

		cout << endl << "Prajes si pokracovat?   (1.) ano | (0.) nie : " << endl;
		cin >> vyber;

		if (vyber != 1) break;
	}

	
	delete kriterium_nazov;
	delete kriterium_po;
	delete kriterium_zast;

	
	
}