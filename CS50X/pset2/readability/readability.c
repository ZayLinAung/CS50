#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string input);
int count_words(string input);
int count_sen(string input);


int main (void){
    string text = get_string("Text: ");
    int letters = count_letters(text);
    int words = count_words(text);
    int sen = count_sen(text);
    printf("%i\n", letters);
    printf("%i\n", words);
    printf("%i\n", sen);
    
    float L = (100/(float)words) * letters;
    float S = (100/(float)words) * sen;
    printf("%f\n", L);
    printf("%f\n", S);
    
    int grade = round(0.0588 * L - 0.296 * S - 15.8);
    if(grade<1){
        printf("Before Grade 1\n");
    }
    else if(grade>=16){
        printf("Grade 16+\n");
    }
    else{
        printf("Grade %i\n", grade);
    }
    
}



int count_letters(string input){
    int m = 0;
    for (int i = 0,n =strlen(input); i<n; i++){
        if((int) toupper(input[i]) >=65 && (int) toupper(input[i]) <=95){
        m++;
        }
    }
    return m;
}

int count_words(string input){
    int word = 1;
    for(int i = 0, n = strlen(input); i<n; i++){
        if((int) toupper(input[i]) == 32){
            word++;
        }
    }
    return word;
}

int count_sen(string input){
    int sen = 0;
    for(int i = 0,n =strlen(input); i<n; i++){
        if((int) toupper(input[i]) == 33 || (int) toupper(input[i]) == 46 || (int) toupper(input[i]) == 63){
            sen++;
        }
    }
    return sen;
}