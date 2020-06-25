#include <iostream>
#include <string>
#include <Windows.h>
#include <tchar.h>


void TestRead() {
    HANDLE file_handle;
    file_handle = CreateFile(_T(".\\test.txt"), GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, 0);

    if (file_handle == INVALID_HANDLE_VALUE)
    {
        DWORD err = GetLastError();
        if (err == 2) {
            std::cout << "File not found\n";
        }
        else {
            std::cout << "error: " << GetLastError() << "\n";
        }

        return;
    }

    DWORD file_size = GetFileSize(file_handle, NULL);
    std::cout << "File size: " << file_size << "\n";
    //std::cout << "File contents: " << "\n";

    BYTE buf[128] = { 0 };

    ReadFile(file_handle, &buf, 128, 0, NULL);
    //printf("%s\n-----------\n", buf);

    CloseHandle(file_handle);
}

int _tmain(int argc, _TCHAR* argv[])
{
    HANDLE currentThread = GetCurrentThread();
    std::cout << "Target.exe process id: ";
    std::cout << GetProcessIdOfThread(currentThread);
    std::cout << "\n";
    CloseHandle(currentThread);

    std::string value;
    while (true)
    {
        std::cout << "Press <enter> to readfile (Ctrl-C to exit): ";
        std::getline(std::cin, value);
        TestRead();
    }
    return 0;
}