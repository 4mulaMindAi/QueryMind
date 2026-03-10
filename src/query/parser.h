#pragma once

#include <iostream>
#include <vector>
#include <string>
#include "lexer.h"

using namespace std;

struct SelectStatement {
    vector<string> columns;
    string table;
    string condition;
};

struct InsertStatement {
    string table;
    vector<string> values;
};

class Parser {
private:
    vector<Token> tokens;
    int pos;

    Token current() {
        return tokens[pos];
    }

    Token consume() {
        return tokens[pos++];
    }

    bool match(TokenType type) {
        if (current().type == type) {
            pos++;
            return true;
        }
        return false;
    }

public:
    Parser(vector<Token>& t) {
        tokens = t;
        pos    = 0;
    }

    SelectStatement parseSelect() {
        SelectStatement stmt;
        consume();  // SELECT skip

        if (current().type == STAR) {
            stmt.columns.push_back("*");
            consume();
        } else {
            stmt.columns.push_back(current().value);
            consume();
            while (current().type == COMMA) {
                consume();
                stmt.columns.push_back(current().value);
                consume();
            }
        }

        match(FROM);
        stmt.table = current().value;
        consume();

        if (current().type == WHERE) {
            consume();
            string col = current().value; consume();
            string op  = current().value; consume();
            string val = current().value; consume();
            stmt.condition = col + " " + op + " " + val;
        }

        return stmt;
    }

    InsertStatement parseInsert() {
        InsertStatement stmt;
        consume();  // INSERT skip
        match(INTO);

        stmt.table = current().value;
        consume();

        match(VALUES);
        match(LPAREN);

        while (current().type != RPAREN && current().type != END) {
            if (current().type != COMMA)
                stmt.values.push_back(current().value);
            consume();
        }

        return stmt;
    }

    void parse() {
        if (current().type == SELECT) {
            SelectStatement stmt = parseSelect();
            cout << "\n--- Parsed SELECT ---" << endl;
            cout << "Table   : " << stmt.table << endl;
            cout << "Columns : ";
            for (auto& col : stmt.columns) cout << col << " ";
            cout << endl;
            if (!stmt.condition.empty())
                cout << "Where   : " << stmt.condition << endl;

        } else if (current().type == INSERT) {
            InsertStatement stmt = parseInsert();
            cout << "\n--- Parsed INSERT ---" << endl;
            cout << "Table  : " << stmt.table << endl;
            cout << "Values : ";
            for (auto& v : stmt.values) cout << v << " ";
            cout << endl;
        }
    }
};