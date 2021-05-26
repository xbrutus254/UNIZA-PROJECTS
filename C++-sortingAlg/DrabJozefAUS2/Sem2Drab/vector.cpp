#include "vector.h"
#include "ds_routines.h"
#include <cstdlib>
#include <cstring>

namespace structures {

	Vector::Vector(size_t size) :
		memory_(calloc(size, 1)),
		size_(size)
	{
	}

	Vector::Vector(const Vector& other) :
		Vector(other.size_)
	{
		memcpy(memory_, other.memory_, size_);
	}

	Vector::~Vector()
	{
		free(memory_);
		memory_ = nullptr;
		size_ = 0;
	}

	Structure* Vector::clone() const
	{
		return new Vector(*this);
	}

	size_t Vector::size() const
	{
		return size_;
	}

	Structure& Vector::operator=(const Structure& other)
	{
		if (this != &other)
		{
			*this = dynamic_cast<const Vector&>(other);
		}
		return *this;
	}

	Vector& Vector::operator=(const Vector& other)
	{
		if (this != &other) {
			this->size_ = other.size_;
			this->memory_ = realloc(this->memory_, this->size_);
			memcpy(this->memory_, other.memory_, this->size_);
		}
		return *this;
	}

	bool Vector::operator==(const Vector& other) const
	{
		return this->size_ == other.size_ && memcmp(this->memory_, other.memory_, this->size_) == 0;
	}

	byte& Vector::operator[](const int index)
	{
		DSRoutines::rangeCheckExcept(index, size_, "Out of range!");
		return *(reinterpret_cast<byte*>(memory_) + index);
	}

	byte Vector::operator[](const int index) const
	{
		DSRoutines::rangeCheckExcept(index, size_, "Out of range!");
		return *(reinterpret_cast<byte*>(memory_) + index);

	}

	byte& Vector::readBytes(const int index, const int count, byte& destination)
	{
		if (count > 0) {
			DSRoutines::rangeCheckExcept(index, this->size_, "Vector::readBytes : Out of range!");
			DSRoutines::rangeCheckExcept(index + count - 1, this->size_, "Vector::readBytes : Out of range!");
			if ((this->getBytePointer(index) <= &destination && &destination < this->getBytePointer(index + count)) || (&destination <= this->getBytePointer(index) && this->getBytePointer(index) < &destination + index)) {
				memmove(&destination, this->getBytePointer(index), count);
			}
			else {
				memcpy(&destination, this->getBytePointer(index), count);
			}
		}
		return destination;
	}

	void Vector::copy(const Vector& src, const int srcStartIndex, Vector& dest, const int destStartIndex, const int length)
	{


		DSRoutines::rangeCheckExcept(srcStartIndex, src.size_, "Vector::copy : Out of range!");
		DSRoutines::rangeCheckExcept(destStartIndex, dest.size_, "Vector::copy : Out of range!");
		memcpy(reinterpret_cast<byte*>(dest.memory_) + destStartIndex, reinterpret_cast<byte*>(src.memory_) + srcStartIndex, length);

	}

	byte* Vector::getBytePointer(const int index) const
	{

		DSRoutines::rangeCheckExcept(index, size_, "Vector::getBytePointer : Out of range!");
		return reinterpret_cast<byte*>(memory_) + index; 
	}

}