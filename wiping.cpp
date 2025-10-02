#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>
#include <cstdio>       // for remove()
#include <string>
#include <filesystem>   // C++17 filesystem API

namespace fs = std::filesystem;
using namespace std;

// Function to wipe a single file
bool wipeFile(const string &filePath, int passes = 3) {
    srand(static_cast<unsigned>(time(0))); // RNG seed

    fstream file(filePath, ios::in | ios::out | ios::binary);
    if (!file) {
        cerr << "❌ Error: Cannot open file " << filePath << endl;
        return false;
    }

    file.seekg(0, ios::end);
    streampos fileSize = file.tellg();
    file.seekg(0, ios::beg);

    // Overwrite passes
    for (int pass = 1; pass <= passes; ++pass) {
        file.seekp(0, ios::beg);
        for (streampos i = 0; i < fileSize; ++i) {
            char randomByte = static_cast<char>(rand() % 256);
            file.write(&randomByte, 1);
        }
        file.flush();
        cout << "Pass " << pass << "/" << passes << " completed for " << filePath << endl;
    }

    file.close();

    // Delete file
    if (remove(filePath.c_str()) == 0) {
        cout << "✅ " << filePath << " wiped securely (" 
             << passes << "-pass overwrite)." << endl;
        return true;
    } else {
        cerr << "❌ Error: Could not delete file " << filePath << endl;
        return false;
    }
}

// Function to wipe all files in a folder (recursively)
void wipeFolder(const string &folderPath, int passes = 3) {
    try {
        for (const auto &entry : fs::recursive_directory_iterator(folderPath)) {
            if (fs::is_regular_file(entry.path())) {
                wipeFile(entry.path().string(), passes);
            }
        }
        cout << "📂 Folder wiping completed for: " << folderPath << endl;
    } catch (const exception &e) {
        cerr << "❌ Error wiping folder: " << e.what() << endl;
    }
}

int main() {
    string target;
    int passes;

    cout << "Enter file/folder/drive path to wipe: ";
    getline(cin, target);

    cout << "Enter number of overwrite passes (e.g., 3): ";
    cin >> passes;

    if (fs::is_regular_file(target)) {
        wipeFile(target, passes);
    } else if (fs::is_directory(target)) {
        wipeFolder(target, passes);
    } else {
        cout << "❌ Invalid path: " << target << endl;
    }

    return 0;
}

