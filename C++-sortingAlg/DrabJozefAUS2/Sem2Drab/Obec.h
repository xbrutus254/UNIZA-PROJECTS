#pragma once
#include "UzemnaJedn.h"


using namespace std;

class Obec : public UzemnaJednotka {
public:
	Obec(string nazov_obce);
	~Obec();
};

Obec::Obec(string nazov_obce)
{
	set_nazov_uj(nazov_obce);
}

Obec::~Obec()
{
}