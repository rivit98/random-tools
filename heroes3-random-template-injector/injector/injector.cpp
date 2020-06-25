#include <iostream>
#include <string>
#include <cstring>
#include <Windows.h>
#include <tchar.h>
#include <tlhelp32.h>
#include <stdio.h>

#include <easyhook.h>


int getProcessId(const std::string& search_name) {
	int pid = 0;
	std::wstring to_search(search_name.begin(), search_name.end());

	HANDLE snap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
	if (snap == INVALID_HANDLE_VALUE) {
		printf("%d", GetLastError());
	}

	PROCESSENTRY32 pe32;
	pe32.dwSize = sizeof(PROCESSENTRY32);

	if (!Process32First(snap, &pe32)) {
		printf("%d", GetLastError());
		CloseHandle(snap);
	}

	do {
		std::wstring s(pe32.szExeFile);

		if (s == to_search) {
			pid = pe32.th32ProcessID;
			break;
		}

	} while (Process32Next(snap, &pe32));

	CloseHandle(snap);

	return pid;
}

int _tmain(int argc, _TCHAR* argv[])
{
	//std::string to_inject("target.exe");
	std::string to_inject("h3hota.exe");

	DWORD processId = getProcessId(to_inject);
	std::cout << to_inject << " ---> " << processId << "\n";

	WCHAR dllToInject[] = L".\\hookdll.dll";
	wprintf(L"Attempting to inject: %s\n", dllToInject);

	NTSTATUS nt = RhInjectLibrary(
		processId,   // The process to inject into
		0,           // ThreadId to wake up upon injection
		EASYHOOK_INJECT_DEFAULT,
		dllToInject, // 32-bit
		NULL,		 // 64-bit not provided
		NULL, // data to send to injected DLL entry point
		0// size of data to send
	);

	if (nt != 0)
	{
		std::cout << "RhInjectLibrary failed with error code = %d" << nt << "\n";
		PWCHAR err = RtlGetLastErrorString();
		std::wcout << err << "\n";
	}
	else
	{
		std::cout << "Library injected successfully\n";
	}

	return 0;
}