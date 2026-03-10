#include <iostream>
#include "query/lexer.h"

using namespace std;

int main() {

    string query = "SELECT * FROM users WHERE id = 5";
    cout << "Query : " << query << endl;
    cout << "\n--- Tokens ---" << endl;

    Lexer lexer(query);
    vector<Token> tokens = lexer.tokenize();

    for (auto& token : tokens) {
        if (token.type == END) break;
        cout << "Type: " << token.type 
             << "  Value: " << token.value << endl;
    }

    return 0;
}