#pragma once

#include <iostream>
#include <vector>

using namespace std;

#define ORDER 4  // max 4 children per node

struct BTreeNode {
    vector<int> keys;
    vector<BTreeNode*> children;
    bool is_leaf;

    BTreeNode(bool leaf) {
        is_leaf = leaf;
    }
};

class BPlusTree {
private:
    BTreeNode* root;

    // node split karo jab overflow ho
    void splitChild(BTreeNode* parent, int i, BTreeNode* child) {
        BTreeNode* newNode = new BTreeNode(child->is_leaf);
        int mid = ORDER / 2;

        // right half naye node mein
        for (int j = mid + 1; j < (int)child->keys.size(); j++)
            newNode->keys.push_back(child->keys[j]);

        if (!child->is_leaf) {
            for (int j = mid + 1; j < (int)child->children.size(); j++)
                newNode->children.push_back(child->children[j]);
        }

        int midKey = child->keys[mid];

        child->keys.resize(mid);
        if (!child->is_leaf)
            child->children.resize(mid + 1);

        parent->children.insert(parent->children.begin() + i + 1, newNode);
        parent->keys.insert(parent->keys.begin() + i, midKey);
    }

    void insertNonFull(BTreeNode* node, int key) {
        int i = node->keys.size() - 1;

        if (node->is_leaf) {
            node->keys.push_back(0);
            while (i >= 0 && key < node->keys[i]) {
                node->keys[i + 1] = node->keys[i];
                i--;
            }
            node->keys[i + 1] = key;
        } else {
            while (i >= 0 && key < node->keys[i]) i--;
            i++;
            if ((int)node->children[i]->keys.size() == ORDER - 1) {
                splitChild(node, i, node->children[i]);
                if (key > node->keys[i]) i++;
            }
            insertNonFull(node->children[i], key);
        }
    }

    // key search karo
    bool search(BTreeNode* node, int key) {
        int i = 0;
        while (i < (int)node->keys.size() && key > node->keys[i]) i++;

        if (i < (int)node->keys.size() && key == node->keys[i])
            return true;

        if (node->is_leaf) return false;

        return search(node->children[i], key);
    }

    void print(BTreeNode* node, int level) {
        cout << "Level " << level << " : ";
        for (int k : node->keys) cout << k << " ";
        cout << endl;

        if (!node->is_leaf)
            for (auto child : node->children)
                print(child, level + 1);
    }

public:
    BPlusTree() {
        root = new BTreeNode(true);
    }

    void insert(int key) {
        if ((int)root->keys.size() == ORDER - 1) {
            BTreeNode* newRoot = new BTreeNode(false);
            newRoot->children.push_back(root);
            splitChild(newRoot, 0, root);
            root = newRoot;
        }
        insertNonFull(root, key);
    }

    bool find(int key) {
        return search(root, key);
    }

    void print() {
        print(root, 0);
    }
};