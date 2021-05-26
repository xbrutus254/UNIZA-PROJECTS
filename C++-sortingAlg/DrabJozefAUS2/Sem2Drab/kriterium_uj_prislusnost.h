#pragma once

#include "krit_uzemna_jednotka.h"
#include "UzemnaJedn.h"

class Kriterium_uj_prislusnost : public Kriterium_uzemnej_j<bool>
{
public:
	Kriterium_uj_prislusnost(UzemnaJednotka* p_uj);
	~Kriterium_uj_prislusnost() {};
	bool ohodnot(UzemnaJednotka* o) override;
private:
	UzemnaJednotka* uj;
};

Kriterium_uj_prislusnost::Kriterium_uj_prislusnost(UzemnaJednotka* p_uj)
{
	uj = p_uj;
}

bool Kriterium_uj_prislusnost::ohodnot(UzemnaJednotka* o)
{
	if (o == nullptr) {
		return false;
	}
	else {
		if (o->get_parent() != nullptr) {
			if (o->get_parent()->get_nazov_uj() == uj->get_nazov_uj()) return true;
		}
		if (o->get_parent()->get_parent() != nullptr) {
			if (o->get_parent()->get_parent()->get_nazov_uj() == uj->get_nazov_uj()) return true;
		}
	}
	return false;
}
