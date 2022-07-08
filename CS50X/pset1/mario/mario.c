#include <cs50.h>
#include <stdio.h>

int main (void)

{
    int i;
    do
    {
        i=get_int("Height: ");
    }
    while(i<1 || i>8);
    
   int x,y,z,p;
    for(y=0; y<i; y++)
    {
        for(z=0; z <i-y-1 ;z++)
        {
            printf(" ");
        }
        for(x=0; x<y+1; x++)
        {
            printf("#");
        }
        printf("  ");
        for(p=0; p<y+1; p++)
        {
            printf("#");
        }
    printf("\n");
    }
}
    