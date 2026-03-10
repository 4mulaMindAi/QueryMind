#pragma once

#include <vector>
#include <string>
#include "lexer.h"

using namespace std;

// SELECT query ka structure
struct SelectStatement {
    vector<string> columns;   // SELECT ke baad kya hai
    string table;             // FROM ke baad kya hai
    string condition;         // WHERE ke baad kya hai
};

// INSERT query ka structure
struct InsertStatement {
    string table;             // INTO ke baad kya hai
    vector<string> values;    // VALUES ke baad kya hai
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

    // SELECT parse karo
    SelectStatement parseSelect() {
        SelectStatement stmt;
        consume();  // SELECT skip karo

        // columns padho
        if (current().type == STAR) {
            stmt.columns.push_back("*");
            consume();
        } else {
            stmt.columns.push_back(current().value);
            consume();
            while (current().type == COMMA) {
                consume();  // comma skip
                stmt.columns.push_back(current().value);
                consume();
            }
        }

        // FROM
        match(FROM);
        stmt.table = current().value;
        consume();

        // WHERE (optional)
        if (current().type == WHERE) {
            consume();  // WHERE skip
            string col = current().value; consume();
            string op  = current().value; consume();
            string val = current().value; consume();
            stmt.condition = col + " " + op + " " + val;
        }

        return stmt;
    }

    // INSERT parse karo
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

public:
    Parser(vector<Token>& t) {
        tokens = t;
        pos    = 0;
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