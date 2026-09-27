/*
 * CSE 3206 | Lab 3 | Group 6 | Pattern: Command
 * File   : EditorInvoker.h
 * Author : Roll 138
 * Role   : Invoker - executes commands and manages undo/redo history
 */
#ifndef EDITOR_INVOKER_H
#define EDITOR_INVOKER_H

#include <iostream>
#include <memory>
#include <stack>
#include <utility>
#include "Command.h"

class EditorInvoker {
private:
    std::stack<std::unique_ptr<Command>> undoStack;
    std::stack<std::unique_ptr<Command>> redoStack;

public:
    void executeCommand(std::unique_ptr<Command> command) {
        command->execute();
        std::cout << "   Executed : " << command->describe() << "\n";
        undoStack.push(std::move(command));
        redoStack = std::stack<std::unique_ptr<Command>>();   // a new action clears redo history
    }

    void undo() {
        if (undoStack.empty()) {
            std::cout << "   Nothing to undo.\n";
            return;
        }
        std::unique_ptr<Command> command = std::move(undoStack.top());
        undoStack.pop();
        command->undo();
        std::cout << "   Undone   : " << command->describe() << "\n";
        redoStack.push(std::move(command));
    }

    void redo() {
        if (redoStack.empty()) {
            std::cout << "   Nothing to redo.\n";
            return;
        }
        std::unique_ptr<Command> command = std::move(redoStack.top());
        redoStack.pop();
        command->execute();
        std::cout << "   Redone   : " << command->describe() << "\n";
        undoStack.push(std::move(command));
    }

    std::size_t historySize() const { return undoStack.size(); }
};

#endif
