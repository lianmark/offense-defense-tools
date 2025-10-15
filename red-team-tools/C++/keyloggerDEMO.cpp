# JFF project
#include <conio.h>
#include <list>
#include <fstream> 
#include <iostream> 
using namespace std;

int main(){
    list<char> mylist;
    while(true)
    {
        char key = _getch();
        printf("You pressed %c\n ", key);
        mylist.push_back(key);
        if(key == 'q')
        {
            break;
        }
    };

    ofstream filetxt("testkeylogger.txt");
    if(filetxt.is_open()){
        for(auto n = mylist.begin(); n != mylist.end(); ++n)
    {
        filetxt << *n;
        if(*n == ' '){ filetxt << endl;}
    } 

    }
    else{
        cerr << "error"; 
    }
    filetxt.close();
}
