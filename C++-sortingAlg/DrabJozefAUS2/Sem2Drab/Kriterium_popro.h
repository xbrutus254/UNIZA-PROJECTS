#pragma once
#include "krit_uzemna_jednotka.h"
#include "UzemnaJedn.h"

class Kriterium_popro : public Kriterium_uzemnej_j<int>
{
public:
	Kriterium_popro() : Kriterium_uzemnej_j() {};
	//~Kriterium_uj_nazov : Kriterium_uzemnej_j();
	int ohodnot(UzemnaJednotka* o) override;

};

int Kriterium_popro::ohodnot(UzemnaJednotka* o)
{
	return o->get_po_pro();
}
