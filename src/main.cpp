#include <iostream>
#include <string>
#include "query/executor.h"

using namespace std;

void printWelcome() {
    cout << "╔════════════════════════════════════╗" << endl;
    cout << "║         QueryMind v1.0             ║" << endl;
    cout << "║   Intelligent Database Engine      ║" << endl;
    cout << "║        4mulaMindAI 🧠              ║" << endl;
    cout << "╚════════════════════════════════════╝" << endl;
    cout << "\nType 'help' for commands, 'exit' to quit\n" << endl;
}

void printHelp() {
    cout << "\n--- Commands ---" << endl;
    cout << "CREATE users id name age    → table banao" << endl;
    cout << "INSERT INTO t VALUES (...)  → row daalo" << endl;
    cout << "SELECT * FROM t             → sab dekho" << endl;
    cout << "SELECT * FROM t WHERE c = v → filter karo" << endl;
    cout << "exit                        → band karo\n" << endl;
}

int main() {

    Executor db;
    string input;

    printWelcome();

    // demo table already ready
    db.createTable("users", {"id", "name", "age"});
    db.execute("INSERT INTO users VALUES (1, Alice, 22)");
    db.execute("INSERT INTO users VALUES (2, Bob, 25)");
    db.execute("INSERT INTO users VALUES (3, Charlie, 22)");

    cout << "\nDemo table 'users' ready!\n" << endl;

    while (true) {
        cout << "QueryMind> ";
        getline(cin, input);

        if (input == "exit") {
            cout << "\nGoodbye! 👋" << endl;
            break;
        } else if (input == "help") {
            printHelp();
        } else if (input.substr(0, 6) == "CREATE") {
            // CREATE users id name age
            // simple table creation
            vector<string> cols;
            string word = "";
            int spaceCount = 0;
            string tableName = "";

            for (int i = 0; i < (int)input.size(); i++) {
                if (input[i] == ' ') {
                    spaceCount++;
                    if (spaceCount == 2) tableName = word;
                    else if (spaceCount > 2) cols.push_back(word);
                    word = "";
                } else {
                    word += input[i];
                }
            }
            if (!word.empty()) cols.push_back(word);

            db.createTable(tableName, cols);
        } else if (input.empty()) {
            continue;
        } else {
            db.execute(input);
        }
    }

    return 0;
}