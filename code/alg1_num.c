#include <iostream>
#include <time.h>
#include <unistd.h>


using namespace std;

int main(int,char**)
{
    timespec start_t,end_t;
    clock_gettime(CLOCK_MONOTONIC,&start_t);

    //usleep(1005);  //sleep(int) 在unix下为秒为单位

    for (int i(1);i < 5;++i)
        for (int j(1);j < 5;++j)
            for (int k(1);k < 5;++k)
               for (int l(1);l < 5;++l)
               {
                   cout << i << j << k << l << endl;
               }
    clock_gettime(CLOCK_MONOTONIC,&end_t);

    cout  << "running time(ns):" << end_t.tv_nsec - start_t.tv_nsec << endl;

    return 0;
}
