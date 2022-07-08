#include <cs50.h>
#include <stdio.h>

int main (void)
{
    int height;
    do
    {
        height=get_int("Whats the height?");
    }
    while(height<1 || height>8);
    
    int row,hash,space;
    for(row=0; row<height; row++)
    {
        for(space=0; space<height-row-1; space++)
        {
            printf(" ");
        }
        for(hash=0; hash<row+1; hash++)
        {
            printf("#");
        }
        printf("\n");
    }
}