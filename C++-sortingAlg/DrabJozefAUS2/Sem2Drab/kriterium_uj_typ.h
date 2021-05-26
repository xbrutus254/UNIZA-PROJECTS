#pragma once

#include "krit_uzemna_jednotka.h"
#include "UzemnaJedn.h"
#include "Typ_UJ.h"

using namespace Typ_uj;

class Kriterium_uj_typ : public Kriterium_uzemnej_j<Typ_uz_jedn>
{
public:
	Kriterium_uj_typ() : Kriterium_uzemnej_j() {};
	//~Kriterium_uj_nazov : Kriterium_uzemnej_j();
	Typ_uz_jedn ohodnot(UzemnaJednotka* o) override;

};

Typ_uz_jedn Kriterium_uj_typ::ohodnot(UzemnaJednotka* o)
{
	if (o->get_parent() == nullptr) {
		return Typ_uz_jedn::kraj;
	}
	else if (o->get_parent() != nullptr && o->get_parent()->get_parent() == nullptr) {
		return Typ_uz_jedn::okres;
	}
	else {
		return Typ_uz_jedn::obec;
	}

}