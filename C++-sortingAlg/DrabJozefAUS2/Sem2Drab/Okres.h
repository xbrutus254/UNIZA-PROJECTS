#pragma once

#include "UzemnaJedn.h"

class Okres : public UzemnaJednotka {
public:
	Okres(string nazov_okresu);
	~Okres();
};

Okres::Okres(string nazov_okresu)
{
	set_nazov_uj(nazov_okresu);
}

Okres::~Okres()
{
}