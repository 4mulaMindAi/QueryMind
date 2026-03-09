#include <iostream>
#include "storage/btree.h"

using namespace std;

int main() {

    BPlusTree tree;

    // 10 numbers insert karo
    for (int i = 1; i <= 10; i++)
        tree.insert(i * 10);

    // tree print karo
    cout << "--- B+ Tree Structure ---" << endl;
    tree.print();

    // search karo
    cout << "\n40 found : " << (tree.find(40) ? "Yes" : "No") << endl;
    cout << "99 found : " << (tree.find(99) ? "Yes" : "No") << endl;

    return 0;
}