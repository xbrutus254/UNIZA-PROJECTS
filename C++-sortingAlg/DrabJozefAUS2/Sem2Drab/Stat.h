#pragma once

#include "sorted_sequence_table.h"
#include "UzemnaJedn.h"
#include "CSV_loading.h"

#include "Kraj.h"
#include "Okres.h"
#include "Obec.h"
#include <iostream>
#include <string>

#include <io.h>
#include <fcntl.h>
#include <locale>

using namespace std;
using namespace structures;


class Stat : public UzemnaJednotka
{
private:
	SortedSequenceTable<string, UzemnaJednotka*>* tabulka_krajov = nullptr;
	SortedSequenceTable<string, UzemnaJednotka*>* tabulka_okresov = nullptr;
	SortedSequenceTable<string, UzemnaJednotka*>* tabulka_obci = nullptr;
public:
	Stat();
	~Stat();

	UzemnaJednotka& pridaj_kraj(string nazov);
	UzemnaJednotka& pridaj_okres(string nazov, UzemnaJednotka* parent);
	void pridaj_obec(string nazov, UzemnaJednotka* parent);
	UzemnaJednotka* get_obec(string nazov);
	SortedSequenceTable<string, UzemnaJednotka*>* get_obce();
	SortedSequenceTable<string, UzemnaJednotka*>* get_okresy();
	SortedSequenceTable<string, UzemnaJednotka*>* get_kraje();
	
	void vypis_kraje();
	void vypis_okresy();
	void vypis_obce();
	



};
//------------------------------------------------------------------------//
Stat::Stat()
{
	//set_nazov_uj("Slovensko");
	tabulka_krajov = new SortedSequenceTable<string, UzemnaJednotka*>();
	tabulka_okresov = new SortedSequenceTable<string, UzemnaJednotka*>();
	tabulka_obci = new SortedSequenceTable<string, UzemnaJednotka*>();
}

Stat::~Stat()
{
	for (auto* temp : *tabulka_krajov) {
		delete temp->accessData();
	}
	delete tabulka_krajov;

	for (auto* temp : *tabulka_okresov) {
		delete temp->accessData();
	}
	delete tabulka_okresov;

	for (auto* temp : *tabulka_obci) {
		delete temp->accessData();
	}
	delete tabulka_obci;
}
//------------------------------------------------------------------------//
SortedSequenceTable<string, UzemnaJednotka*>* Stat::get_obce() {
	return tabulka_obci;
}
SortedSequenceTable<string, UzemnaJednotka*>* Stat::get_okresy() {
	return tabulka_okresov;
}
SortedSequenceTable<string, UzemnaJednotka*>* Stat::get_kraje() {
	return tabulka_krajov;
}


//------------------------------------------------------------------------//
UzemnaJednotka& Stat::pridaj_kraj(string nazov)
{
	
	if ((tabulka_krajov->containsKey(nazov)))
	{
		//cout << "existujuci " << nazov << endl;
		return *(*tabulka_krajov)[nazov];
	}
	else {
		//cout << "neeeexistujuci " << nazov << endl;
		UzemnaJednotka* uzem_jedn = new Kraj(nazov);
		uzem_jedn->set_parent(this);
		tabulka_krajov->insert(uzem_jedn->get_nazov_uj(), uzem_jedn);
		return *uzem_jedn;
	}

}

UzemnaJednotka& Stat::pridaj_okres(string nazov, UzemnaJednotka* parent)
{
	if ((tabulka_okresov->containsKey(nazov)))
	{
		return *(*tabulka_okresov)[nazov];
	}
	else {
		UzemnaJednotka* uzem_jedn = new Okres(nazov);
		uzem_jedn->set_parent(parent);
		tabulka_okresov->insert(uzem_jedn->get_nazov_uj(), uzem_jedn);
		return *uzem_jedn;
	}
	
}

void Stat::pridaj_obec(string nazov, UzemnaJednotka* parent)
{
	if (!(tabulka_obci->containsKey(nazov)))
	{

		UzemnaJednotka* uzem_jedn = new Obec(nazov);
		uzem_jedn->set_parent(parent);
		tabulka_obci->insert(uzem_jedn->get_nazov_uj(), uzem_jedn);
	}
	
}

UzemnaJednotka* Stat::get_obec(string nazov)
{
	for (auto temp : *tabulka_obci)
	{
		if (temp->getKey() == nazov) {
			return temp->accessData();
		}
		
	}
	return nullptr;
}


void Stat::vypis_kraje()
{
	for (auto* uzem_j : *tabulka_krajov)
	{
		cout << uzem_j->getKey() << " " << uzem_j->accessData()->get_vymera() << endl;
	}
}

void Stat::vypis_okresy()
{
	for (auto* uzem_j : *tabulka_okresov)
	{
		cout << uzem_j->getKey() << " " << uzem_j->accessData()->get_parent()->get_nazov_uj() << endl;
	}
}

void Stat::vypis_obce()
{
	for (auto* uzem_j : *tabulka_obci)
	{
		cout << uzem_j->getKey() << " okres: " << uzem_j->accessData()->get_parent()->get_nazov_uj() << " kraj: " << uzem_j->accessData()->get_parent()->get_parent()->get_nazov_uj();
		cout << "   |  vymera: " << uzem_j->accessData()->get_vymera() << endl;
	}
}

