/*
 * Project: getAddresses / memory scanner (WIP)
 * Author: Lian Mark
 *
 * Note: Beginner in C++. This project is educational / experimental.
 * Significant portions of the code and guidance were developed with AI-assisted
 * support (the assistant provided snippets and debugging tips).
 *
 * Use only in controlled lab environments and for lawful, ethical purposes.
 */
 /*
 * EDUCATIONAL USE ONLY — DO NOT USE ILLEGALLY
 *
 * This code is provided for learning and testing in controlled environments only.
 * Do NOT use it to access, control, or damage systems or data you do not own
 * or do not have explicit written permission to test.
 *
 * Unauthorized or illegal use is prohibited — you are solely responsible for
 * any consequences. This is not legal advice.
 */
#include <iostream>
#include <map>
#include <istream>
#include <vector>
#include <Windows.h>
#include <psapi.h>
using namespace std;

int main() {

    DWORD pid = 19364;                      // change to target PID

    HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, pid);
    if (!hProcess) { cerr << "OpenProcess failed " << GetLastError() << "\n"; return 1; }

    // char name[MAX_PATH];
    // DWORD nameLen = MAX_PATH;
    // if (QueryFullProcessImageNameA(hProcess, 0, name, &nameLen)) cout << name << "\n";

    SYSTEM_INFO sysInfo;
    GetSystemInfo(&sysInfo);
    vector<string> InterestingAddresses;
    MEMORY_BASIC_INFORMATION mbi;
    int target;
    int newValue = 1000;
    map<uintptr_t, int> INaddresses;
    while (true)
    {
    cout << "Enter target" << endl;
    cin >> target;
        LPBYTE addr = (LPBYTE)sysInfo.lpMinimumApplicationAddress;
        while (addr < (LPBYTE)sysInfo.lpMaximumApplicationAddress) {
            SIZE_T q = VirtualQueryEx(hProcess, addr, &mbi, sizeof(mbi));
            if (q == 0) { addr += sysInfo.dwPageSize; continue; }   // skip by page size on failure

            if (mbi.State == MEM_COMMIT) {
                DWORD prot = mbi.Protect;
                bool readable = (prot & PAGE_READONLY) || (prot & PAGE_READWRITE) ||
                                (prot & PAGE_EXECUTE_READ) || (prot & PAGE_EXECUTE_READWRITE) ||
                                (prot & PAGE_WRITECOPY);
                if (readable) {
                    SIZE_T regionSize = (SIZE_T)mbi.RegionSize;
                    vector<unsigned char> buf(regionSize);                 // simple: read whole region
                    SIZE_T bytesRead = 0;
                    if (ReadProcessMemory(hProcess, mbi.BaseAddress, buf.data(), regionSize, &bytesRead) && bytesRead >= sizeof(int)) {
                        for (SIZE_T i = 0; i + sizeof(int) <= bytesRead; ++i) {
                            int v = *reinterpret_cast<int*>(buf.data() + i);
                            if (v == target) {
                                uintptr_t found = (uintptr_t)mbi.BaseAddress + i;
                                // cout << hex << (void*)found << dec << "\n";
                                uintptr_t written = 0;
                                INaddresses[found]++;
                                if (INaddresses[found] > 5)
                                {
                                    cout << "Possible Address match: " << hex << (void*)found << dec << " count=" << INaddresses[found] <<endl;
                                    WriteProcessMemory(hProcess, (LPVOID)found, &newValue, sizeof(newValue), &written);
                                } 
                            }
                        }
                    }
                }
            }
            addr = (LPBYTE)mbi.BaseAddress + mbi.RegionSize;
        }
    }        CloseHandle(hProcess);
        return 0;
}
