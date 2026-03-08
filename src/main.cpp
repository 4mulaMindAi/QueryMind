#include <iostream>
#include "storage/page.h"

using namespace std;

int main() {

    Page p;
    p.page_id = 1;

    string msg = "Hello QueryMind!";
    for (int i = 0; i < (int)msg.size(); i++)
        p.data[i] = msg[i];

    cout << "Page ID  : " << p.page_id  << endl;
    cout << "Data     : " << p.data     << endl;
    cout << "Is Dirty : " << p.is_dirty << endl;

    return 0;
}