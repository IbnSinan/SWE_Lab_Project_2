/*
 * CSE 3206 | Lab 3 | Group 6 | Pattern: Command
 * File   : main.cpp
 * Author : Roll 138
 * Role   : Client (part 2) - interactive editor menu and program entry
 *
 * Scenario: Mini Text Editor with Undo / Redo
 *
 * Build: g++ -std=c++17 -Wall -o text_editor main.cpp
 */
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include "Demo.h"

using namespace std;

void runInteractive() {
    TextEditor editor;
    EditorInvoker invoker;

    cout << "\n--- Interactive editor ---\n";
    while (true) {
        cout << "\n1) Write  2) Delete  3) Undo  4) Redo  0) Exit\nChoice: ";
        int choice;
        if (!(cin >> choice) || choice == 0) {
            break;
        }
        try {
            if (choice == 1) {
                string words;
                cout << "Text to write: ";
                cin.ignore();
                getline(cin, words);
                invoker.executeCommand(make_unique<WriteCommand>(editor, words));
            } else if (choice == 2) {
                int count;
                cout << "Characters to delete: ";
                cin >> count;
                if (count < 0) {
                    throw invalid_argument("Delete count cannot be negative.");
                }
                invoker.executeCommand(make_unique<DeleteCommand>(editor, static_cast<size_t>(count)));
            } else if (choice == 3) {
                invoker.undo();
            } else if (choice == 4) {
                invoker.redo();
            } else {
                cout << "   Invalid choice.\n";
            }
        } catch (const invalid_argument& e) {
            cout << "   [ERROR] " << e.what() << "\n";
        }
        show(editor);
        cout << "   History  : " << invoker.historySize() << " command(s)\n";
    }
}

int main() {
    cout << "===== Mini Text Editor (Command Pattern) =====\n";
    runDemo();
    runInteractive();
    cout << "\nGoodbye!\n";
    return 0;
}
