#pragma once
#include "krit_uzemna_jednotka.h"
#include "UzemnaJedn.h"

class Kriterium_pocet_obyv : public Kriterium_uzemnej_j<int>
{
public:
	Kriterium_pocet_obyv() : Kriterium_uzemnej_j() {};
	~Kriterium_pocet_obyv() {};
	int ohodnot(UzemnaJednotka* o) override;

};

int Kriterium_pocet_obyv::ohodnot(UzemnaJednotka* o)
{
	return (o->get_pred_pro() + o->get_pro() + o->get_po_pro());
	//return o->get_nazov_uj();
}
//--------------------------------------------------------------------
