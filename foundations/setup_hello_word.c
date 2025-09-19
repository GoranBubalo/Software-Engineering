#include <stdio.h>

int main() {

    char name[50];

    printf("Hello, Goran!\n");
    
    printf("Enter your last name: ");
    scanf("%49s", name);
    printf("Gorans last name is %s, welcomme to c programming\n", name);
}