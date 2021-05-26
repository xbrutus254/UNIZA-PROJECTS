#pragma once
#include "krit_uzemna_jednotka.h"
#include "UzemnaJedn.h"

class Kriterium_predpro : public Kriterium_uzemnej_j<int>
{
public:
	Kriterium_predpro() : Kriterium_uzemnej_j() {};
	//~Kriterium_uj_nazov : Kriterium_uzemnej_j();
	int ohodnot(UzemnaJednotka* o) override;

};

int Kriterium_predpro::ohodnot(UzemnaJednotka* o)
{
	return o->get_pred_pro();
}


