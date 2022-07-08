#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main (int argc, string argv[]){
    char check[26];
    if(argc == 2){
        for(int i = 0, n = strlen(argv[1]); i<n; i++){
            if(isalpha (argv[1][i]) && n== 26){
                 check[i] = toupper (argv[1][i]);
                for(int j = -1; j<i;j++){
                    if(check[i] == check[j]){
                    printf("Key must not contain repeated characters.\n");
                    return 1;
                    }
                }
                
            }
            else if(n != 26){
                printf("Key must contains 26 characters.\n");
                return 1;
            }
            else{
                printf("Key must only contain alphabetic characters.\n");
                return 1;
            }
        }
    }
    
    else{
        printf("Usage: ./substitution key\n");
        return 1;
    }
    
    
    string text = get_string("plaintext: ");
    printf("ciphertext: ");
    
    for (int i = 0, n = strlen(text); i<n; i++){
        if(isalpha (text[i])){
             if(islower (text[i])){
                 printf("%c", tolower (check[text[i]- 97]));
            }
            else if(isupper (text[i])){
                printf("%c", toupper (check[text[i] - 65]));
            }
        }
        else{
            printf("%c", text[i]);
        }
    }
    
    printf("\n");
    return 0;
}


