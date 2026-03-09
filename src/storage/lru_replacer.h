#pragma once

#include <list>
#include <unordered_map>

using namespace std;

class LRUReplacer {
private:
    int capacity;
    list<int> lru_list;                          // front = most recent
    unordered_map<int, list<int>::iterator> map; // page_id → position

public:
    LRUReplacer(int capacity) {
        this->capacity = capacity;
    }

    // page access hua — use recent mark karo
    void access(int page_id) {
        if (map.find(page_id) != map.end())
            lru_list.erase(map[page_id]);        // purani position hatao

        lru_list.push_front(page_id);            // front mein daalo
        map[page_id] = lru_list.begin();
    }

    // sabse purana page nikalo — evict karo
    int evict() {
        if (lru_list.empty()) return -1;

        int oldest = lru_list.back();            // sabse purana
        map.erase(oldest);
        lru_list.pop_back();
        return oldest;
    }

    int size() {
        return lru_list.size();
    }
};