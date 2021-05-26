// Sem2Drab.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "CSV_loading.h"
#include "Heap_monitor.h"
#include "Stat.h"
//#include "kriterium_uj_nazov.h"
#include "uroven1.h"
#include "uroven2.h"


int main()
{
    initHeapMonitor();
    std::cout << "nacitavam csv..\n";
    CSV_loader* loader = new CSV_loader();
    cout << "-----------------" << endl;
    Stat* stat = loader->get_stat();

    int vyber = -1;
    while (1) {
        cout << endl << "Zadaj ktoru funkcionalitu chces robit:" << endl;
        cout << "(1.) Vypis info o uzemnych jednotkach" << endl;
        cout << "(2.) Zoradenie uzemnych jednotiek" << endl;


        cin >> vyber;
        if (vyber == 1) {
            Uroven1* u1 = new Uroven1(stat);
            delete u1;
        }
        else if (vyber == 2) {
            uroven2* u2 = new uroven2(stat);
            delete u2;
        }

        cout << endl << "prajes si skoncit? " << endl;
        cout << "(1.) Ano" << endl;
        cout << "(0.) Nie" << endl;
        cin >> vyber;

        if (vyber == 1) break;
    }


    //u1->spust();
    //stat->vypis_obce();
    //cout << Kriterium_uj_nazov().ohodnot(stat->get_obec("Sabinov")) << endl;
    delete loader;

}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
