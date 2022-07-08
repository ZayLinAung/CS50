#include <cs50.h>
#include <stdio.h>

int main (void)
{
    long long credit= get_long("Type your credit card number here: ");
    long long int credit_1=credit;
    long long int credit_2=credit;
    long long int credit_3=credit;
    
    int remaindr,answer,answer1,answer2,remaindr1,remaindr2,product;
    int save=0;
     while(credit>=1)
    {
        
        remaindr= credit%10;
        credit=credit/10;
        
    
    
        remaindr1=credit%10;
        remaindr1=remaindr1*2;
        credit=credit/10;
        
        
        if(remaindr1>=10)
        {
            remaindr2=remaindr1%10;
            answer1=remaindr1/10;
            remaindr1=remaindr2+answer1;
        }
        product=remaindr+remaindr1;
        save= save+product;
    }
    int length=0;
    while(credit_1>=1)
    {
        credit_1=credit_1/10;
        length++;
    }
    
    while(credit_2>=100)
    {
        credit_2=credit_2/10;
    }
    
    while(credit_3>=10)
    {
        credit_3=credit_3/10;
    }
    
    int verify= save%10;
    
    if(verify==0 && length==15 && (credit_2==34 || credit_2==37))
    {
        printf("AMEX\n");
    }
    else if(verify==0 && length==16 && (credit_2==51 || credit_2==52 || credit_2==53 || credit_2==54 || credit_2==55))
    {
        printf("MASTERCARD\n");
    }
    else if(verify==0 && (length==13 || length==16) && credit_3==4)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}


    
    
