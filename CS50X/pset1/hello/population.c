#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size

    // TODO: Prompt for end size

    // TODO: Calculate number of years until we reach threshold

    // TODO: Print number of years
    int n;
    do
    { n= get_int("The initial value: ");}
    while(n<9);
    
    int x;
    do
    { x=get_int("The final value: ");}
    while(x<n);
    
    int years = 0;
    while(n<x)
    {
        n=n + (n/3) - (n/4);
        years++;
    }
    printf("Years: %i\n", years);
   }