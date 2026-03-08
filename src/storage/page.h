#pragma once

using namespace std;

#define PAGE_SIZE 4096

class Page {
public:
    char data[PAGE_SIZE];
    int page_id;
    bool is_dirty;
    int pin_count;

    Page() {
        page_id   = -1;
        is_dirty  = false;
        pin_count = 0;
        for (int i = 0; i < PAGE_SIZE; i++) 
            data[i] = 0;
    }

    void clear() {
        for (int i = 0; i < PAGE_SIZE; i++) 
            data[i] = 0;
    }
};