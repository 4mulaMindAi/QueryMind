#pragma once

#include <unordered_map>
#include "page.h"
#include "disk_manager.h"
#include "lru_replacer.h"

using namespace std;

class BufferPoolManager {
private:
    int pool_size;
    Page* pages;
    DiskManager* disk;
    LRUReplacer* replacer;
    unordered_map<int, int> page_table;  // page_id → frame_id
    list<int> free_frames;               // khali frames

public:
    BufferPoolManager(int size, DiskManager* disk) {
        this->pool_size = size;
        this->disk      = disk;
        pages           = new Page[size];
        replacer        = new LRUReplacer(size);

        for (int i = 0; i < size; i++)
            free_frames.push_back(i);   // sab frames khali hain
    }

    // page fetch karo — memory mein hai toh wahan se, nahi toh disk se
    Page* fetchPage(int page_id) {
        // memory mein hai?
        if (page_table.find(page_id) != page_table.end()) {
            int frame_id = page_table[page_id];
            replacer->access(frame_id);
            pages[frame_id].pin_count++;
            return &pages[frame_id];
        }

        // memory mein nahi — frame chahiye
        int frame_id = getFrame();
        if (frame_id == -1) return nullptr;  // koi frame nahi mila

        // disk se padho
        disk->readPage(page_id, &pages[frame_id]);
        pages[frame_id].page_id  = page_id;
        pages[frame_id].pin_count = 1;
        page_table[page_id]      = frame_id;
        replacer->access(frame_id);

        return &pages[frame_id];
    }

    // naya page banao
    Page* newPage(int& page_id) {
        int frame_id = getFrame();
        if (frame_id == -1) return nullptr;

        page_id = disk->allocatePage();
        pages[frame_id].page_id   = page_id;
        pages[frame_id].pin_count = 1;
        pages[frame_id].is_dirty  = false;
        pages[frame_id].clear();

        page_table[page_id] = frame_id;
        replacer->access(frame_id);

        return &pages[frame_id];
    }

    // page unpin karo — use karna band kiya
    bool unpinPage(int page_id, bool is_dirty) {
        if (page_table.find(page_id) == page_table.end()) return false;

        int frame_id = page_table[page_id];
        pages[frame_id].pin_count--;
        pages[frame_id].is_dirty = is_dirty;

        return true;
    }

    // page disk pe save karo
    bool flushPage(int page_id) {
        if (page_table.find(page_id) == page_table.end()) return false;

        int frame_id = page_table[page_id];
        disk->writePage(page_id, &pages[frame_id]);
        pages[frame_id].is_dirty = false;

        return true;
    }

    ~BufferPoolManager() {
        delete[] pages;
        delete replacer;
    }

private:
    // khali frame dhundo
    int getFrame() {
        if (!free_frames.empty()) {
            int frame_id = free_frames.front();
            free_frames.pop_front();
            return frame_id;
        }

        // koi khali frame nahi — LRU se evict karo
        int frame_id = replacer->evict();
        if (frame_id == -1) return -1;

        // agar dirty hai toh disk pe save karo
        Page* page = &pages[frame_id];
        if (page->is_dirty)
            disk->writePage(page->page_id, page);

        page_table.erase(page->page_id);
        return frame_id;
    }
};