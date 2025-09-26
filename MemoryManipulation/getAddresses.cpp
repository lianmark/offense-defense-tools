#include <iostream> // Include the iostream library for input/output operations
#include <map>
#include <istream>
#include <vector>
#include <Windows.h>
#include <psapi.h>
using namespace std;

// class Player{
//     private:
//         string name;
//         int health;
//     public:
//         Player(string n, int h){
//         name = n;
//         health = h;
//         }
//     int takeDamage(int dmg){
//         health = health - dmg;
//     return health;
//     }
//     void stats(){
//         cout << "Name chosen: " << name << " Current HP: " << health << endl; 
//     }
// };
// int add(int a, int b){
//     return a + b;
// };
// int subtract(int a, int b){
//     return a - b;
// };
int main() { // The main function, where program execution begins
    // string name = "Lian";
    // cout << "Hello my name is " << name << " and I am learning c++!" << endl;

    // int birtyear;
    // cout << "Enter your year of birth ";
    // cin >> birtyear;
    // cout <<"You are:"<< 2026 - birtyear << " Years old" << endl;  

    // int secretNumber;
    // cout << "Enter secret number: " << endl;
    // cin >>  secretNumber;
    // if (secretNumber == 23){
    //     cout << "You win!"<< endl;
    // }else {
    //     cout << "Wrong, try again."<< endl;
    // }
    // string input;
    // cout << "Choose subtract or add function:";
    // cin >> input;
    // if(input == "subtract"){
    //     int x;
    //     int y;
    //     cin >> x;
    //     cin >> y;
    //     cout << subtract(x, y) << endl;
    // }
    // if(input == "add"){
    //     int n, r;
    //     cin >> n;
    //     cin >> r;
    //     cout << add(n,r) << endl;
    // }
     
    // string movies[5] = {"LOTR", "Hobbit", "It", "Aragon", "Left 4 Dead"};
    // for(int i = 0; i < 5; i++){
    //     cout << movies[i] << endl;
    // }

    // //step 6... i dont remember :(
    // Player p1("Lian", 100);
    // p1.stats();
    // p1.takeDamage(20);
    // p1.stats();

    // Player Aragon("Knight", 200);
    // Aragon.stats();
    // Aragon.takeDamage(50);
    // Aragon.stats();

    // vector<string> companies;
    // companies.push_back("Lian");
    // companies.push_back("John");
    // companies.push_back("Connor");
    // cout << companies[0] << endl;
    DWORD pid = 2196;                      // change to target PID

    // HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, pid);
    // if (!hProcess) { cerr << "OpenProcess failed " << GetLastError() << "\n"; return 1; }

    // char name[MAX_PATH];
    // DWORD nameLen = MAX_PATH;
    // if (QueryFullProcessImageNameA(hProcess, 0, name, &nameLen)) cout << name << "\n";

    SYSTEM_INFO sysInfo;
    GetSystemInfo(&sysInfo);

    MEMORY_BASIC_INFORMATION mbi;
    int target;
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
                                cout << hex << (void*)found << dec << "\n";
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
