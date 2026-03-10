#pragma once

#include <iostream>
#include <vector>
#include <unordered_map>
#include "parser.h"

using namespace std;

struct Row {
    unordered_map<string, string> data;
};

struct Table {
    string name;
    vector<string> columns;
    vector<Row> rows;
};

class Executor {
private:
    unordered_map<string, Table> tables;

public:
    void createTable(const string& name, vector<string> cols) {
        Table t;
        t.name    = name;
        t.columns = cols;
        tables[name] = t;
        cout << "Table '" << name << "' created!" << endl;
    }

    void insert(InsertStatement& stmt) {
        if (tables.find(stmt.table) == tables.end()) {
            cout << "Error: Table not found!" << endl;
            return;
        }

        Table& t = tables[stmt.table];
        Row row;

        for (int i = 0; i < (int)t.columns.size(); i++) {
            if (i < (int)stmt.values.size())
                row.data[t.columns[i]] = stmt.values[i];
        }

        t.rows.push_back(row);
        cout << "1 row inserted into '" << stmt.table << "'!" << endl;
    }

    void select(SelectStatement& stmt) {
        if (tables.find(stmt.table) == tables.end()) {
            cout << "Error: Table not found!" << endl;
            return;
        }

        Table& t = tables[stmt.table];

        cout << "\n";
        for (auto& col : t.columns)
            cout << col << "\t";
        cout << "\n";
        for (int i = 0; i < 30; i++) cout << "-";
        cout << "\n";

        for (auto& row : t.rows) {
            if (!stmt.condition.empty()) {
                string col = stmt.condition.substr(0, stmt.condition.find(' '));
                string val = stmt.condition.substr(stmt.condition.rfind(' ') + 1);
                if (row.data.find(col) != row.data.end())
                    if (row.data.at(col) != val) continue;
            }

            for (auto& col : t.columns)
                cout << row.data.at(col) << "\t";
            cout << "\n";
        }
    }

    void execute(const string& query) {
        Lexer lexer(query);
        auto tokens = lexer.tokenize();
        Parser parser(tokens);

        if (tokens[0].type == SELECT) {
            SelectStatement stmt = parser.parseSelect();
            select(stmt);
        } else if (tokens[0].type == INSERT) {
            InsertStatement stmt = parser.parseInsert();
            insert(stmt);
        }
    }
};