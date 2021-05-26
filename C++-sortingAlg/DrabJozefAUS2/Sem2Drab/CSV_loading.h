#pragma once
#include "UzemnaJedn.h"
#include "Stat.h"

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

using namespace std;
using namespace structures;

//using namespace structures;

class CSV_loader
{
private:
	Stat* stat = nullptr;
	long long celkovo = 0;
	long long celkovoKE = 0;
	void nacitaj_clenenie();
	void nacitaj_obce();


public:
	CSV_loader();
	~CSV_loader();

	
	void process_obce(string line);
	void process_clenenie(string line);
	Stat* get_stat();
};

Stat* CSV_loader::get_stat() {
	return stat;
}

CSV_loader::~CSV_loader()
{
	delete stat;
}

//#####################################################
CSV_loader::CSV_loader()
{
	nacitaj_clenenie();
	nacitaj_obce();
}

void CSV_loader::nacitaj_clenenie()
{
	//1 Obce SR.csv
	//cout << "nacitavam clenenie " << endl;
	stat = new Stat();
	string csvfile_name = "2 Územné èlenenie SR.csv";
	ifstream file(csvfile_name);
	int index_word = 0;
	int index_line = 0;

	string line = "";
	string word = "";

	while (getline(file, line))
	{
		if (index_line == 0)	// prvy riadok skipp
		{
			//cout << line << endl;
			index_line++;
			continue;
		}
		process_clenenie(line);

		index_line++;
	}
}

void CSV_loader::nacitaj_obce()
{
	
	//cout << "nacitavam obce " << endl;
	string csvfile_name = "1 Obce SR.csv";
	ifstream file(csvfile_name);
	int index_word = 0;
	int index_line = 0;

	string line = "";
	string word = "";

	while (getline(file, line))
	{
		if (index_line == 0)	// prvy riadok skipp
		{
			//cout << line << endl;
			index_line++;
			continue;
		}
		process_obce(line);

		index_line++;
	}
}


void CSV_loader::process_obce(string line)
{
	//Obec;Predproduktívni obyvatelia;Produktívni obyvatelia;Poproduktívni obyvatelia;Celková výmera (v m2);Zastavaná plocha (v m2)
	string word = "";
	int index_word = 0;
	stringstream splitter(line);
	string nazov_obce = "";
	int pred_pro = 0;
	int pro = 0;
	int po_pro = 0;
	int vymera = 0;
	int plocha = 0;

	while (getline(splitter, word, ';'))	// rozdelovac line podla ;
	{
		if (index_word == 0) { // Obec
			nazov_obce = word;
		}
		else if (index_word == 1) { // pred_pro
			pred_pro = stoi(word);
		}
		else if (index_word == 2) { // pro
			pro = stoi(word);
		}
		else if (index_word == 3) { // po_pro
			po_pro = stoi(word);
		}
		else if (index_word == 4) { // vymera
			vymera = stoi(word);
		}
		else if (index_word == 5) { // plocha
			if (word.back() == ',') {
				word = word.substr(0, word.size() - 1);
			}
			plocha = stoi(word);
		}

		index_word++;
	}
	
	UzemnaJednotka* uj = stat->get_obec(nazov_obce);
	uj->set_pred_pro(pred_pro);
	uj->set_pro(pro);
	uj->set_po_pro(po_pro);
	uj->set_vymera(vymera);
	uj->set_zast_plocha(plocha);
	

	//cout << "obec: " << uj->get_nazov_uj() << " | get_pred_pro: " << uj->get_pred_pro() << endl;

	
	// okres
	UzemnaJednotka* uj_okres = uj->get_parent();
	uj_okres->set_pred_pro(uj_okres->get_pred_pro()+uj->get_pred_pro());
	uj_okres->set_pro(uj_okres->get_pro() + uj->get_pro());
	uj_okres->set_po_pro(uj_okres->get_po_pro() + uj->get_po_pro());
	uj_okres->set_vymera(uj_okres->get_vymera() + uj->get_vymera());
	uj_okres->set_zast_plocha(uj_okres->get_zast_plocha() + uj->get_zast_plocha());

	// kraj
	UzemnaJednotka* uj_kraj = uj_okres->get_parent();
	uj_kraj->set_pred_pro(uj_kraj->get_pred_pro() + uj->get_pred_pro());
	uj_kraj->set_pro(uj_kraj->get_pro() + uj->get_pro());
	uj_kraj->set_po_pro(uj_kraj->get_po_pro() + uj->get_po_pro());
	uj_kraj->set_vymera((uj_kraj->get_vymera() + uj->get_vymera()));
	uj_kraj->set_zast_plocha((uj_kraj->get_zast_plocha() + uj->get_zast_plocha()));
}

void CSV_loader::process_clenenie(string line)
{
	//Názov obce;Názov okresu;Názov kraja
	string word = "";
	int index_word = 0;
	stringstream splitter(line);
	string obec = "";
	string okres = "";
	string kraj = "";

	while (getline(splitter, word, ';'))	// rozdelovac line podla ;
	{
		if (index_word == 0) 	// Obec
		{
			//cout << word << endl;
			obec = word;
		}
		else if (index_word == 1) // okresu
		{
			//cout << word << endl;
			okres = word;
		}
		else if (index_word == 2) // kraj
		{
			//cout << word << endl;
			if (word.back() == ',') {
				word = word.substr(0, word.size() - 1);
			}
			kraj = word;
		}

		index_word++;
	}

	
	UzemnaJednotka& otec_kraj = stat->pridaj_kraj(kraj);
	UzemnaJednotka& otec_okres = stat->pridaj_okres(okres, &otec_kraj);
	stat->pridaj_obec(obec, &otec_okres);

}