#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main (void)
{
    float change;
    do
    {
    change=get_float("Whats your amount of dollar?");
    }
    while(change<=0);
    int cents= round(change*100);
    
   
    int quarter=25;
    int dime=10;
    int nickle=5;
    int penny=1;
    int number=0;
    int r;
    
    while(quarter<=cents)
    {
        r= cents % quarter;
        number= (cents-r)/quarter;
        cents= r;
    }
    
    while(dime<=cents)
    {
        r= cents % dime;
        number=number + (cents-r)/dime;
        cents=r;
    }
      while(nickle<=cents)
    {
        r= cents % nickle;
        number=number + (cents-r)/nickle;
        cents=r;
    }
      while(penny<=cents)
    {
        r= cents % penny;
        number=number + (cents-r)/penny;
        cents=r;
    }
    
    printf("The number of coins are %i\n", number);
}