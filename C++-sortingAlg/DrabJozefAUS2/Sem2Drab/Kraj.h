#pragma once
#include "UzemnaJedn.h"

class Kraj : public UzemnaJednotka {
public:
	Kraj(string nazov);
	~Kraj();
};

Kraj::Kraj(string nazov)
{
	set_nazov_uj(nazov);
}

Kraj::~Kraj()
{
}