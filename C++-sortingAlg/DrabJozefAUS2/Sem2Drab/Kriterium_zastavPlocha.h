#pragma once
#include "krit_uzemna_jednotka.h"
#include "UzemnaJedn.h"

class Kriterium_zastavPlocha : public Kriterium_uzemnej_j<double>
{
public:
	Kriterium_zastavPlocha() : Kriterium_uzemnej_j() {};
	//~Kriterium_uj_nazov : Kriterium_uzemnej_j();
	double ohodnot(UzemnaJednotka* o) override;

};

double Kriterium_zastavPlocha::ohodnot(UzemnaJednotka* o)
{
	return (double)(100 * (double)o->get_zast_plocha() / (double)o->get_vymera());
}
