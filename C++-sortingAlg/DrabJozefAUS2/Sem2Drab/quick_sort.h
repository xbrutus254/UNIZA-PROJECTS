#pragma once

#include "sort.h"
#include "unsorted_sequence_table.h"



namespace structures
{

	/// <summary> Triedenie Quick sort. </summary>
	/// <typeparam name = "K"> Kluc prvkov v tabulke. </typepram>
	/// <typeparam name = "T"> Typ dat ukladanych v tabulke. </typepram>
	template <typename K, typename T>
	class QuickSort : public Sort<K, T>
	{
	private: 
		void quick(UnsortedSequenceTable<K, T>& table, int startIndex, int endIndex);
		void quick_r(UnsortedSequenceTable<K, T>& table, int startIndex, int endIndex);
	public:
		/// <summary> Utriedi tabulku triedenim Quick sort. </summary>
		/// <param name = "table"> NonortedSequenceTable, ktoru ma utriedit. </param>
		void sort(UnsortedSequenceTable<K, T>& table) override;
		void sort_r(UnsortedSequenceTable<K, T>& table);
	};

	template<typename K, typename T>
	inline void QuickSort<K, T>::quick(UnsortedSequenceTable<K, T>& table, int startIndex, int endIndex)
	{
		K pivot = table.getItemAtIndex(startIndex + (endIndex - startIndex) / 2).getKey();

		int leftIndex = startIndex;
		int rightIndex = endIndex;
		while (leftIndex <= rightIndex) {
			while (table.getItemAtIndex(leftIndex).getKey() < pivot) {
				
				leftIndex++;
				//cout << table.getItemAtIndex(leftIndex).getKey() << " ? " << pivot << endl;
			}
			
			while (table.getItemAtIndex(rightIndex).getKey() > pivot) {
				//cout << table.getItemAtIndex(leftIndex).getKey() << endl;
				rightIndex--;
			}

			//table.swap(leftIndex, rightIndex);

			if (leftIndex <= rightIndex) {
				table.swap(leftIndex, rightIndex);
				leftIndex++;
				rightIndex--;

			}
		}
		if (startIndex < rightIndex) {
			quick(table, startIndex, rightIndex);

		}

		if (leftIndex < endIndex) {
			quick(table, leftIndex, endIndex);

		}

	}

	template<typename K, typename T>
	inline void QuickSort<K, T>::quick_r(UnsortedSequenceTable<K, T>& table, int startIndex, int endIndex)
	{
		K pivot = table.getItemAtIndex(startIndex + (endIndex - startIndex) / 2).getKey();

		int leftIndex = startIndex;
		int rightIndex = endIndex;
		while (leftIndex <= rightIndex) {
			while (table.getItemAtIndex(leftIndex).getKey() > pivot) {

				leftIndex++;
				//cout << table.getItemAtIndex(leftIndex).getKey() << " ? " << pivot << endl;
			}

			while (table.getItemAtIndex(rightIndex).getKey() < pivot) {
				//cout << table.getItemAtIndex(leftIndex).getKey() << endl;
				rightIndex--;
			}

			//table.swap(leftIndex, rightIndex);

			if (leftIndex <= rightIndex) {
				table.swap(leftIndex, rightIndex);
				leftIndex++;
				rightIndex--;
				//Sort<K, T>::notify();
			}
		}
		if (startIndex < rightIndex) {
			quick_r(table, startIndex, rightIndex);

		}

		if (leftIndex < endIndex) {
			quick_r(table, leftIndex, endIndex);

		}

	}

	template<typename K, typename T>
	inline void QuickSort<K, T>::sort(UnsortedSequenceTable<K, T>& table)
	{
		quick(table, 0, table.size() - 1);
	}

	template<typename K, typename T>
	inline void QuickSort<K, T>::sort_r(UnsortedSequenceTable<K, T>& table)
	{
		quick_r(table, 0, table.size() - 1);
	}

}