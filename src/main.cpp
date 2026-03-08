#include <iostream>
#include "storage/page.h"
#include "storage/disk_manager.h"

using namespace std;

int main() {

    DiskManager disk("queryMind.db");

    Page p1;
    p1.page_id = disk.allocatePage();
    string msg = "Day 2 - Disk Manager working!";
    for (int i = 0; i < (int)msg.size(); i++)
        p1.data[i] = msg[i];

    disk.writePage(p1.page_id, &p1);
    cout << "Page " << p1.page_id << " writting page 1" << endl;

    Page p2;
    disk.readPage(0, &p2);
    cout << "Reading from disk : " << p2.data << endl;

    return 0;
}