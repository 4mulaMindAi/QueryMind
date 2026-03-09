#include <iostream>
#include "storage/page.h"
#include "storage/disk_manager.h"
#include "storage/buffer_pool.h"
#include "storage/btree.h"

using namespace std;

int main() {

    // Storage layer setup
    DiskManager disk("queryMind.db");
    BufferPoolManager bpm(5, &disk);

    // B+ Tree setup
    BPlusTree tree;

    // 20 records insert karo
    cout << "--- Inserting Records ---" << endl;
    for (int i = 1; i <= 20; i++) {
        // tree mein insert karo
        tree.insert(i * 5);

        // page mein bhi store karo
        int pid;
        Page* p = bpm.newPage(pid);
        if (p != nullptr) {
            string record = "Record " + to_string(i * 5);
            for (int j = 0; j < (int)record.size(); j++)
                p->data[j] = record[j];
            bpm.unpinPage(pid, true);
            bpm.flushPage(pid);
        }
    }
    cout << "20 records insert ho gaye!" << endl;

    // Tree structure dekho
    cout << "\n--- B+ Tree Structure ---" << endl;
    tree.print();

    // Search karo
    cout << "\n--- Searching ---" << endl;
    cout << "25 found : " << (tree.find(25) ? "Yes" : "No") << endl;
    cout << "55 found : " << (tree.find(55) ? "Yes" : "No") << endl;
    cout << "99 found : " << (tree.find(99) ? "Yes" : "No") << endl;

    // Page fetch karo disk se
    cout << "\n--- Fetching from Disk ---" << endl;
    Page* fetched = bpm.fetchPage(0);
    if (fetched != nullptr)
        cout << "Page 0 data : " << fetched->data << endl;

    return 0;
}