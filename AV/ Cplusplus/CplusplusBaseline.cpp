#include <iostream>    
#include <windows.h>   
#include <fstream>    
#include <iomanip>   
#include <string>     
#include <wincrypt.h>  
#include <sstream>    
#include <iomanip>    
#include <vector>     
#include <Softpub.h>  
#include <tchar.h>      

#pragma comment(lib, "Advapi32.lib")  // link against Advapi32 (for crypt API)
#pragma comment(lib, "Crypt32.lib")   // link against Crypt32 (for cert API)
#pragma comment(lib, "Wintrust.lib")  // link against Wintrust (for WinVerifyTrust)

using namespace std; 

// ============================================================================
// NOTE: This particular function was 100% AI-generated (for educational / reference use).
//       Review, test, and adapt before using in production environments.
// ============================================================================
void computeMD5FromFile(const std::wstring &filePath) {
    FILE* fp = _wfopen(filePath.c_str(), L"rb");  // open file in binary mode
    if (!fp) {
        std::wcerr << L"Error: Cannot open file: " << filePath << std::endl;
        return; // if file can’t be opened, exit
    }

    HCRYPTPROV hProv = 0;   // crypto provider handle
    HCRYPTHASH hHash = 0;   // hash object handle

    // Acquire a cryptographic context
    if (!CryptAcquireContextW(&hProv, NULL, NULL, PROV_RSA_FULL, CRYPT_VERIFYCONTEXT)) {
        std::cerr << "CryptAcquireContext failed" << std::endl;
        fclose(fp);
        return;
    }

    // Create an MD5 hash object
    if (!CryptCreateHash(hProv, CALG_MD5, 0, 0, &hHash)) {
        std::cerr << "CryptCreateHash failed" << std::endl;
        CryptReleaseContext(hProv, 0);
        fclose(fp);
        return;
    }

    // Buffer to read chunks of the file
    std::vector<unsigned char> buffer(8192);
    size_t bytesRead;

    // Read the file piece by piece and hash it
    while ((bytesRead = fread(buffer.data(), 1, buffer.size(), fp)) > 0) {
        if (!CryptHashData(hHash, buffer.data(), (DWORD)bytesRead, 0)) {
            std::cerr << "CryptHashData failed" << std::endl;
            CryptDestroyHash(hHash);
            CryptReleaseContext(hProv, 0);
            fclose(fp);
            return;
        }
    }
    fclose(fp); // close file when done

    BYTE rgbHash[16];   // MD5 is 128 bits = 16 bytes
    DWORD cbHash = 16;

    // Get the final MD5 value
    if (CryptGetHashParam(hHash, HP_HASHVAL, rgbHash, &cbHash, 0)) {
        std::ostringstream oss;
        oss << std::hex << std::setfill('0'); // print as hex with padding

        for (DWORD i = 0; i < cbHash; i++) {
            oss << std::setw(2) << (int)rgbHash[i];
        }

        std::cout << "MD5: " << oss.str() << std::endl;  // print MD5
    }

    CryptDestroyHash(hHash);      // cleanup hash object
    CryptReleaseContext(hProv, 0); // cleanup crypto provider
}

// ------------------------------
// Function: scanFolder
// Recursively scans all files and folders
// ------------------------------
void scanFolder(const wstring &folder) {
    WIN32_FIND_DATAW data;              // struct to hold file info
    wstring pattern = folder + L"\\*";  // search pattern: everything in folder
    HANDLE hFind = FindFirstFileW(pattern.c_str(), &data); // start search
    if (hFind == INVALID_HANDLE_VALUE) return; // if folder can’t be opened, exit

    long long counter = 0; // unused here, but could count files
    while (true) { 
        wstring name = data.cFileName; // current item name
    
        if (name != L"." && name != L"..") { // skip special folders
            wstring fullPath = folder + L"\\" + name; // build full path
            bool isDir = (data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) != 0;

            if (isDir && !(data.dwFileAttributes & FILE_ATTRIBUTE_REPARSE_POINT)) {
                // if it's a directory (and not a symlink/junction), go deeper
                scanFolder(fullPath);
            }
            else if (!isDir) {
                // if it's a file → compute MD5
                computeMD5FromFile(fullPath);
                // (signature check will be added later here)
            }
        }
    
        if (!FindNextFileW(hFind, &data)) break; // move to next file
    }
    FindClose(hFind); // cleanup handle
}

// ------------------------------
// main()
// Entry point
// ------------------------------
int main() {
    SetConsoleOutputCP(CP_UTF8);  // make console support UTF-8 output

    string path = "C:\\Users\\PC\\Desktop\\nscs-system\\C++ Anti-virus\\Scan_caches\\BaseScan.dat";
    ofstream file(path, ios::binary | ios::out); // open output file (currently unused)

    WCHAR drives[512];                       // buffer for drive letters
    DWORD len = GetLogicalDriveStringsW(512, drives); // get all drives
    WCHAR* p = drives;                       // pointer to current drive

    while(*p) {
        scanFolder(wstring(p));   // scan each drive
        p += wcslen(p) +1;        // move to next drive string
    }
}
