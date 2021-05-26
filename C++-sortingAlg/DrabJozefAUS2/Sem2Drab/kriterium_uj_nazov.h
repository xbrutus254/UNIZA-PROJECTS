#pragma once
#include "krit_uzemna_jednotka.h"
#include "UzemnaJedn.h"

class Kriterium_uj_nazov : public Kriterium_uzemnej_j<string>
{
public:
	Kriterium_uj_nazov() : Kriterium_uzemnej_j() {};
	//~Kriterium_uj_nazov : Kriterium_uzemnej_j();
	string ohodnot(UzemnaJednotka* o) override;

};

string Kriterium_uj_nazov::ohodnot(UzemnaJednotka* o)
{
	return o->get_nazov_uj();
}

