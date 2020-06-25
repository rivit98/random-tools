#include <string>
#include <iostream>
#include <fstream>

#include <windows.h>
#include <string.h>
#include <psapi.h>
#include <stdio.h>
#include <strsafe.h>
#include <tchar.h>

#include <easyhook.h>


#define BUFSIZE 512

std::ofstream outfile;


std::string getFileNameByHandle(HANDLE h) {
	TCHAR Path[BUFSIZE];
	DWORD dwRet;

	dwRet = GetFinalPathNameByHandle(h, Path, BUFSIZE, VOLUME_NAME_NT);
	if (dwRet < BUFSIZE)
	{
		std::wstring ws(Path);

		return std::string(ws.begin(), ws.end());
	}

	return "Not Found";
}

BOOL WINAPI ReadFileWrapper(
	HANDLE       hFile,
	LPVOID       lpBuffer,
	DWORD        nNumberOfBytesToRead,
	LPDWORD      lpNumberOfBytesRead,
	LPOVERLAPPED lpOverlapped
) {
	std::string fname = getFileNameByHandle(hFile);
	std::string::size_type dot_pos = fname.rfind(".");

	if (dot_pos == std::string::npos) {
		return ReadFile(hFile, lpBuffer, nNumberOfBytesToRead, lpNumberOfBytesRead, lpOverlapped);
	}

	std::string ext = fname.substr(dot_pos);
	if (ext != ".txt") {
		return ReadFile(hFile, lpBuffer, nNumberOfBytesToRead, lpNumberOfBytesRead, lpOverlapped);
	}

	outfile << fname << "\n";
	outfile << nNumberOfBytesToRead << "\n";
	outfile.flush();

	return ReadFile(hFile, lpBuffer, nNumberOfBytesToRead, lpNumberOfBytesRead, lpOverlapped);
}

extern "C" void __declspec(dllexport) __stdcall NativeInjectionEntryPoint(REMOTE_ENTRY_INFO * inRemoteInfo);

void __stdcall NativeInjectionEntryPoint(REMOTE_ENTRY_INFO* inRemoteInfo)
{
	outfile.open("D:\\injected_log.txt", std::ios_base::trunc);
	outfile.close();

	outfile.open("D:\\injected_log.txt", std::ios_base::app);

	outfile << "Injected by process Id: " << inRemoteInfo->HostPID << "\n";
	outfile << GetProcAddress(GetModuleHandle(TEXT("kernel32")), "ReadFile") << "\n";

	HOOK_TRACE_INFO hHook = { NULL };
	NTSTATUS result = LhInstallHook(
		GetProcAddress(GetModuleHandle(TEXT("kernel32")), "ReadFile"),
		ReadFileWrapper,
		NULL,
		&hHook);

	if (FAILED(result))
	{
		std::wstring s(RtlGetLastErrorString());
		outfile << "Failed to install hook: ";
		outfile << std::string(s.begin(), s.end());
		outfile << "\n\nPress any key to exit.";
		return;
	}

	ULONG ACLEntries[1] = { 0 };
	//LhSetInclusiveACL(ACLEntries, 1, &hHook);
	LhSetExclusiveACL(ACLEntries, 1, &hHook);

	outfile.flush();

	return;
}