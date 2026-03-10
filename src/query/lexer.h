#pragma once

#include <string>
#include <vector>

using namespace std;

// Token types — har word ka type
enum TokenType {
    SELECT, FROM, WHERE, INSERT, INTO,
    VALUES, CREATE, TABLE, INT, VARCHAR,
    STAR, COMMA, SEMICOLON, EQUALS,
    LPAREN, RPAREN,
    IDENTIFIER,  // table/column naam
    NUMBER,      // 42, 100
    STRING,      // 'hello'
    END          // query khatam
};

// Ek token = ek word + uska type
struct Token {
    TokenType type;
    string value;

    Token(TokenType t, string v) {
        type  = t;
        value = v;
    }
};

class Lexer {
private:
    string query;
    int pos;

    // whitespace skip karo
    void skipSpaces() {
        while (pos < (int)query.size() && isspace(query[pos]))
            pos++;
    }

    // number padho
    Token readNumber() {
        string num = "";
        while (pos < (int)query.size() && isdigit(query[pos]))
            num += query[pos++];
        return Token(NUMBER, num);
    }

    // word padho
    Token readWord() {
        string word = "";
        while (pos < (int)query.size() && isalnum(query[pos]))
            word += query[pos++];

        // keyword hai ya identifier?
        if (word == "SELECT") return Token(SELECT, word);
        if (word == "FROM")   return Token(FROM, word);
        if (word == "WHERE")  return Token(WHERE, word);
        if (word == "INSERT") return Token(INSERT, word);
        if (word == "INTO")   return Token(INTO, word);
        if (word == "VALUES") return Token(VALUES, word);
        if (word == "CREATE") return Token(CREATE, word);
        if (word == "TABLE")  return Token(TABLE, word);
        if (word == "INT")    return Token(INT, word);

        return Token(IDENTIFIER, word);  // table/column naam
    }

public:
    Lexer(const string& q) {
        query = q;
        pos   = 0;
    }

    // poori query ko tokens mein todo
    vector<Token> tokenize() {
        vector<Token> tokens;

        while (pos < (int)query.size()) {
            skipSpaces();

            if (pos >= (int)query.size()) break;

            char c = query[pos];

            if (isdigit(c)) {
                tokens.push_back(readNumber());
            } else if (isalpha(c)) {
                tokens.push_back(readWord());
            } else if (c == '*') {
                tokens.push_back(Token(STAR, "*")); pos++;
            } else if (c == ',') {
                tokens.push_back(Token(COMMA, ",")); pos++;
            } else if (c == ';') {
                tokens.push_back(Token(SEMICOLON, ";")); pos++;
            } else if (c == '=') {
                tokens.push_back(Token(EQUALS, "=")); pos++;
            } else if (c == '(') {
                tokens.push_back(Token(LPAREN, "(")); pos++;
            } else if (c == ')') {
                tokens.push_back(Token(RPAREN, ")")); pos++;
            } else {
                pos++;  // unknown character skip karo
            }
        }

        tokens.push_back(Token(END, ""));
        return tokens;
    }
};