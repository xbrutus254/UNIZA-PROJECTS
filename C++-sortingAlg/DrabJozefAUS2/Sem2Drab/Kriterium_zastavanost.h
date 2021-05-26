#pragma once
#include "krit_uzemna_jednotka.h"
#include "UzemnaJedn.h"

class Kriterium_zastavanost : public Kriterium_uzemnej_j<long long>
{
public:
	Kriterium_zastavanost() : Kriterium_uzemnej_j() {};
	//~Kriterium_uj_nazov : Kriterium_uzemnej_j();
	long long ohodnot(UzemnaJednotka* o) override;

};

long long Kriterium_zastavanost::ohodnot(UzemnaJednotka* o)
{
	return o->get_zast_plocha();
}
