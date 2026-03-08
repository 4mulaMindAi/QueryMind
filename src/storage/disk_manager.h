#pragma once

#include <fstream>
#include <string>
#include "page.h"

using namespace std;

class DiskManager {
private:
    string   db_file;
    fstream  file;
    int      next_page_id;

public:
    DiskManager(const string& filename) {
        db_file      = filename;
        next_page_id = 0;

        // file nahi hai toh banao, hai toh kholo
        file.open(db_file, ios::in | ios::out | ios::binary);
        if (!file.is_open()) {
            file.clear();
            file.open(db_file, ios::out | ios::binary);
            file.close();
            file.open(db_file, ios::in | ios::out | ios::binary);
        }
    }

    // naya page ka id do
    int allocatePage() {
        return next_page_id++;
    }

    // page ko disk pe likho
    void writePage(int page_id, Page* page) {
        int offset = page_id * PAGE_SIZE;
        file.seekp(offset);
        file.write(page->data, PAGE_SIZE);
        file.flush();
    }

    // disk se page padho
    void readPage(int page_id, Page* page) {
        int offset = page_id * PAGE_SIZE;
        file.seekg(offset);
        file.read(page->data, PAGE_SIZE);
    }

    ~DiskManager() {
        if (file.is_open())
            file.close();
    }
};