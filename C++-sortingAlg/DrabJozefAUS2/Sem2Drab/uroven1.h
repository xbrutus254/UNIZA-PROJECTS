#pragma once
#include "sorted_sequence_table.h"
#include "unsorted_sequence_table.h"

//#include "Stat.h"

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

#include <string>

using namespace std;


class Uroven1
{
public:
	Uroven1(Stat* param_data);
	~Uroven1() {};
	

private:
	Stat* stat_data = nullptr;
	SortedSequenceTable<string, UzemnaJednotka*>* tabulka;
	SortedSequenceTable<int, UzemnaJednotka*>* tabulka_int;
	void spust();
	bool obec = false;
	bool okres = false;
	bool kraj_f = false;
	bool okres_f = false;
	string nazov_kraja = "";
	string nazov_okresu = "";
};


Uroven1::Uroven1(Stat* param_data)
{
	stat_data = param_data;
	int vyber = 4;
	std::cout << endl << "Zadaj co chces testovat:" << endl;
	std::cout << "(1.) Kraje" << endl;
	std::cout << "(2.) Okresy" << endl;
	std::cout << "(3.) Obce" << endl;
	std::cin >> vyber;

	if (vyber == 1)
	{
		tabulka = stat_data->get_kraje();
		std::cout << "zadaj napr. Banskobystricky/Kosicky/Trnavsky" << endl;
		obec = false;
		okres = false;
		spust();
	}
	else if (vyber == 2)
	{
		tabulka = stat_data->get_okresy();
		std::cout << "zadaj napr. Okres Bratislava IV/Okres Kosice - okolie/Okres Senica" << endl;
		obec = false;
		okres = true;
		spust();
	}
	else if (vyber == 3)
	{
		tabulka = stat_data->get_obce();
		std::cout << "zadaj napr. Bratislava - mestska cast Zahorska Bystrica/Sarisske Michalany/Dunajov" << endl;
		obec = true;
		okres = true;
		spust();
	}
	else {
		std::cout << "Zadal si nespravne cislo" << endl;
	}
}

void Uroven1::spust()
{
	bool filter_prisl = false;
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
		filter_prisl = true;
	}


	vyber = 5;
	UnsortedSequenceTable<string, UzemnaJednotka*>* temp = nullptr;
	while (1) {
		std::cout << endl << "Zadaj ktoru ulohu chces robit:" << endl;
		std::cout << "(1.) Filtruj podla nazvu" << endl;
		std::cout << "(2.) Filtruj podla poctu obyv." << endl;
		std::cout << "(3.) Filtruj podla zastavanosti" << endl;

		std::cin >> vyber;
		if (vyber == 1) {
			string nazov_uj = "";

			std::cout << endl << "Zadaj nazov uzemnej jednotky: " << endl;
			while (nazov_uj == "")
				std::getline(std::cin, nazov_uj);
			//cin >> nazov_obce;
			//cout << "nazovvvvvv: " << nazov_obce << endl;

			filter_uj_nazov* filter_nazov = new filter_uj_nazov(nazov_uj);
			temp = filter_nazov->filtruj(tabulka);

			delete filter_nazov;

		}
		else if (vyber == 2) {
			int min = 0;
			int max = 0;
			std::cout << endl << "Zadaj dolnu hranicu : " << endl;
			std::cin >> min;
			std::cout << endl << "Zadaj hornu hranicu : " << endl;
			std::cin >> max;



			filter_obyvatelia* f_obyv = new filter_obyvatelia(min, max);
			temp = f_obyv->filtruj(tabulka);
			delete f_obyv;

		}
		else if (vyber == 3) {
			long long min = 0;
			long long max = 0;
			std::cout << endl << "Zadaj dolnu hranicu : " << endl;
			std::cin >> min;
			std::cout << endl << "Zadaj hornu hranicu : " << endl;
			std::cin >> max;



			filter_zastavanost* f_zastav = new filter_zastavanost(min, max);
			temp = f_zastav->filtruj(tabulka);
			delete f_zastav;

		}

		for (auto l : *temp)
		{
			if (nazov_kraja != "")
			{
				if (obec && okres) {
					if (l->accessData()->get_parent()->get_parent()->get_nazov_uj() != nazov_kraja)
						continue;
				}
				else {
					if (l->accessData()->get_parent()->get_nazov_uj() != nazov_kraja)
						continue;
				}
			}

			else if (nazov_okresu != "")
			{
				if (l->accessData()->get_parent()->get_nazov_uj() != nazov_okresu)
				{
					continue;
				}
			}
			
			//cout << l->getKey() << endl;
			std::cout << "------------------------------------" << endl;
			string nazov = "kraj";
			if (okres && obec) nazov = "obec";
			else if (okres && !obec) nazov = "okres";
			std::cout << nazov <<"  : " << Kriterium_uj_nazov().ohodnot(l->accessData()) << " :" << endl;
			if (okres && obec) {
				std::cout << "okres : " << Kriterium_uj_nazov().ohodnot(l->accessData()->get_parent()) << endl;
				std::cout << "kraj  : " << Kriterium_uj_nazov().ohodnot(l->accessData()->get_parent()->get_parent()) << endl;
			}
			else if (okres && !obec) {
				std::cout << "kraj : " << Kriterium_uj_nazov().ohodnot(l->accessData()->get_parent()) << endl;
			}
			//cout << "okres : " << Kriterium_uj_nazov().ohodnot(l->accessData()->get_parent()) << endl;
			//cout << "kraj  : " << Kriterium_uj_nazov().ohodnot(l->accessData()->get_parent()->get_parent()) << endl;

			std::cout << "  ->  pocet obyvatelov             : " << Kriterium_pocet_obyv().ohodnot(l->accessData()) << endl;
			std::cout << "  ->  pocet predproduktivnych ludi : " << Kriterium_predpro().ohodnot(l->accessData()) << endl;
			std::cout << "  ->  pocet roduktivnych ludi      : " << Kriterium_pro().ohodnot(l->accessData()) << endl;
			std::cout << "  ->  pocet poproduktivnych ludi   : " << Kriterium_popro().ohodnot(l->accessData()) << endl;
			std::cout << "  ->  zastavanost                  : " << Kriterium_zastavanost().ohodnot(l->accessData()) << endl;
			std::cout << "  ->  celkova vymera               : " << Kriterium_celkovaVymera().ohodnot(l->accessData()) << endl;
			std::cout << "  ->  zastavana plocha             : " << (double)Kriterium_zastavPlocha().ohodnot(l->accessData()) << endl;
			std::cout << "------------------------------------" << endl;
		}
		delete temp;
		temp = nullptr;


		std::cout << endl << "Prajes si pokracovat?   (1.) ano | (0.) nie : " << endl;
		std::cin >> vyber;

		if (vyber != 1) break;
	}
	

}