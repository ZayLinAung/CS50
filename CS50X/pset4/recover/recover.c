#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
 
int main(int argc, char *argv[])
{
    
    typedef uint8_t BYTE;
    if (argc != 2)
    {
        printf("Usage: ./recover filename\n");
        return 1;
    }
    
    FILE *file = fopen (argv[1], "r");
    if (file == NULL)
    {
        printf("Cannot open the file.\n");
        return 1;
    }
    
    BYTE buffer[512];
    int counter = 0;
    char *filename;
    FILE *img = NULL;
    
    while (fread(buffer, sizeof(BYTE), 512, file))
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (counter == 0)
            {
                filename = malloc (sizeof(char) * 7);
                sprintf(filename, "%03i.jpg", counter);
                img = fopen (filename, "w");
                fwrite(buffer, sizeof(BYTE), 512, img);
                counter++;
            }
            else
            {
                fclose(img);
                sprintf(filename, "%03i.jpg", counter);
                img = fopen (filename, "w");
                fwrite(buffer, sizeof(BYTE), 512, img);
                counter++;
            }
        }
        else if(counter > 0)
        {
            fwrite(buffer, sizeof(BYTE), 512, img);
        }
    }
    free(filename);
    fclose(img);
    fclose(file);
}