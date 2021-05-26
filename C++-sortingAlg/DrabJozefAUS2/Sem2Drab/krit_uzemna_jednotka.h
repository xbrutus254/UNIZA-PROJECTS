#pragma once

#include "UzemnaJedn.h"
#include "Kriterium.h"

template<typename T>
class Kriterium_uzemnej_j : public Kriterium<UzemnaJednotka, T>
{
public:
	Kriterium_uzemnej_j();
	virtual ~Kriterium_uzemnej_j();
	virtual T ohodnot(UzemnaJednotka* o) = 0;

private:

};

template<typename T>
inline Kriterium_uzemnej_j<T>::Kriterium_uzemnej_j() : Kriterium<UzemnaJednotka, T>::Kriterium()
{
}
template<typename T>
inline Kriterium_uzemnej_j<T>::~Kriterium_uzemnej_j()
{
}
