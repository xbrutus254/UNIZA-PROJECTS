#pragma once

template<typename K, typename T>
class Kriterium
{
public:
	Kriterium();
	virtual ~Kriterium();

	virtual T ohodnot(K* o) = 0;
private:

};

template<typename K, typename T>
inline Kriterium<K, T>::Kriterium()
{
}
template<typename K, typename T>
inline Kriterium<K, T>::~Kriterium()
{
}