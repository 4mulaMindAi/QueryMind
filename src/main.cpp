#include <iostream>
#include "storage/lru_replacer.h"

using namespace std;

int main() {

    LRUReplacer lru(4);   // sirf 4 pages memory mein rakh sakte hain

    lru.access(1);
    lru.access(2);
    lru.access(3);
    lru.access(4);
    lru.access(2);        // page 2 dobara use hua — recent ho gaya

    cout << "Evicted: " << lru.evict() << endl;  // 1 aana chahiye
    cout << "Evicted: " << lru.evict() << endl;  // 3 aana chahiye

    return 0;
}