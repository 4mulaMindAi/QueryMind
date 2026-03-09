#include <iostream>
#include "storage/page.h"
#include "storage/disk_manager.h"
#include "storage/buffer_pool.h"

using namespace std;

int main() {

    DiskManager disk("queryMind.db");
    BufferPoolManager bpm(3, &disk);  // sirf 3 pages memory mein

    // 3 naye pages banao
    int pid1, pid2, pid3;
    Page* p1 = bpm.newPage(pid1);
    Page* p2 = bpm.newPage(pid2);
    Page* p3 = bpm.newPage(pid3);

    // p1 mein data daalo
    string msg = "Buffer Pool Working!";
    for (int i = 0; i < (int)msg.size(); i++)
        p1->data[i] = msg[i];

    bpm.unpinPage(pid1, true);
    bpm.unpinPage(pid2, false);
    bpm.unpinPage(pid3, false);

    // flush karo disk pe
    bpm.flushPage(pid1);
    cout << "Page " << pid1 << " flush hua disk pe!" << endl;

    // wapas fetch karo
    Page* fetched = bpm.fetchPage(pid1);
    cout << "Fetched data : " << fetched->data << endl;

    return 0;
}