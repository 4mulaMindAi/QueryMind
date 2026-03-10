#include <iostream>
#include "query/lexer.h"
#include "query/parser.h"

using namespace std;

int main() {

    // SELECT test
    string q1 = "SELECT * FROM users WHERE id = 5";
    cout << "Query 1 : " << q1 << endl;
    Lexer l1(q1);
    auto tokens1 = l1.tokenize();
    Parser p1(tokens1);
    p1.parse();

    // INSERT test
    string q2 = "INSERT INTO users VALUES (1, 42)";
    cout << "\nQuery 2 : " << q2 << endl;
    Lexer l2(q2);
    auto tokens2 = l2.tokenize();
    Parser p2(tokens2);
    p2.parse();

    return 0;
}