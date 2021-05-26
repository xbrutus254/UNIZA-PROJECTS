#pragma once
#include <string>

using namespace std;
//using namespace structures;

class UzemnaJednotka
{

public:
	UzemnaJednotka* parent = nullptr;
	UzemnaJednotka();
	virtual ~UzemnaJednotka();
	void set_parent(UzemnaJednotka* name);
	UzemnaJednotka* get_parent();

	int get_pred_pro();
	void set_pred_pro(int param);

	int get_pro();
	void set_pro(int param);

	int get_po_pro();
	void set_po_pro(int param);

	long long get_vymera();
	void set_vymera(long long param);

	long long get_zast_plocha();
	void set_zast_plocha(long long param);

	void set_nazov_uj(string nazov);
	string get_nazov_uj();

private:
	string nazov;

	// Predproduktívni obyvatelia
	int pred_pro = 0;
	// Produktívni obyvatelia
	int pro = 0;
	// Poproduktívni obyvatelia
	int po_pro = 0;
	// Celková výmera
	long long vymera = 0;
	// Zastavaná plocha
	long long zast_plocha = 0;

};

UzemnaJednotka::UzemnaJednotka()
{
	parent = nullptr;
}

UzemnaJednotka::~UzemnaJednotka()
{

}

void UzemnaJednotka::set_parent(UzemnaJednotka* name)
{
	parent = name;
}

UzemnaJednotka* UzemnaJednotka::get_parent()
{
	return parent;
}

int UzemnaJednotka::get_pred_pro()
{
	return this->pred_pro;
}
void UzemnaJednotka::set_pred_pro(int param)
{
	//cout << param << endl;
	this->pred_pro = param;
}

int UzemnaJednotka::get_pro()
{
	return this->pro;
}
void UzemnaJednotka::set_pro(int param)
{
	this->pro = param;
}

int UzemnaJednotka::get_po_pro()
{
	return this->po_pro;
}
void UzemnaJednotka::set_po_pro(int param)
{
	this->po_pro = param;
}

long long UzemnaJednotka::get_vymera()
{
	return this->vymera;
}
void UzemnaJednotka::set_vymera(long long param)
{
	this->vymera = (param);
}

long long UzemnaJednotka::get_zast_plocha()
{
	return this->zast_plocha;
}
void UzemnaJednotka::set_zast_plocha(long long param)
{
	this->zast_plocha = (param);
}

void UzemnaJednotka::set_nazov_uj(string nazov)
{
	this->nazov = nazov;
}

string UzemnaJednotka::get_nazov_uj()
{
	return this->nazov;
}