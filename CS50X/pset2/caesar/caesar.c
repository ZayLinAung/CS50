#include<cs50.h>
#include<stdio.h>
#include<string.h>
#include <stdlib.h>
#include <ctype.h>

int main (int argc, string argv[]){
    int key;
    if(argc == 2){
        for(int i = 0, n = strlen(argv[1]); i<n; i++){
            if(isdigit (argv[1][i])){
                key = atoi(argv[1]);
            }
            else{
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
        }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    
    string pt = get_string("plaintext: ");
    printf("ciphertext: ");
    for(int i = 0,n = strlen(pt); i<n; i++){
        int cipher = pt[i]+key;
        if(isalpha (pt[i])){
        if(isupper (pt[i])){
            if(cipher>90){
                int ct = ((cipher-90)%26) + 64;
                printf("%c", ct);
            }
            else{
                printf("%c", cipher);
            }
        }
        else if(islower (pt[i])){
            if(cipher>122){
                int ct = ((cipher-122)%26) + 96;
                printf("%c", ct);
            }
            else{
                printf("%c", cipher);
            }
        }
        
    }
            
        else{
            printf("%c", pt[i]);
        }
    
}
    printf("\n");
    return 0;
}
    
    


