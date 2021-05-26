#pragma once
#include "krit_uzemna_jednotka.h"
#include "UzemnaJedn.h"

class Kriterium_celkovaVymera : public Kriterium_uzemnej_j<long long>
{
public:
	Kriterium_celkovaVymera() : Kriterium_uzemnej_j() {};
	//~Kriterium_uj_nazov : Kriterium_uzemnej_j();
	long long ohodnot(UzemnaJednotka* o) override;

};

long long Kriterium_celkovaVymera::ohodnot(UzemnaJednotka* o)
{
	return o->get_vymera();
}
