#include "helpers.h"
#include <math.h>
#include <stdlib.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int k = 0; k < width-1; k++)
        {
            for (int j = 0; j < width-1-k; j++)
            {
                RGBTRIPLE tmp = image[i][j];
                image[i][j] = image[i][j+1];
                image[i][j+1] = tmp;
            }
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
typedef struct{
        int rgbtRed;
        int rgbtGreen;
        int rgbtBlue;
    }mytype;
    
    mytype newimage[height][width];
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int divider = 0;
            newimage[i][j].rgbtRed = newimage[i][j].rgbtGreen = newimage[i][j].rgbtBlue = 0;
            for (int a = -1; a < 2; a++)
            {
                for (int b = -1; b < 2; b++)
                {
                    if ((j + b >= 0 && j + b < width) && (i + a >= 0 && i + a < height))
                    {
                        newimage[i][j].rgbtRed += image[i+a][j+b].rgbtRed;
                        newimage[i][j].rgbtGreen += image[i+a][j+b].rgbtGreen;
                        newimage[i][j].rgbtBlue += image[i+a][j+b].rgbtBlue;
                        divider++;
                    }
                }
            }
            newimage[i][j].rgbtRed = round(newimage[i][j].rgbtRed / (float)divider);
            newimage[i][j].rgbtGreen = round(newimage[i][j].rgbtGreen / (float)divider);
            newimage[i][j].rgbtBlue = round(newimage[i][j].rgbtBlue / (float)divider);
        }
    }
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = newimage[i][j].rgbtRed;
            image[i][j].rgbtBlue = newimage[i][j].rgbtBlue;
            image[i][j].rgbtGreen = newimage[i][j].rgbtGreen;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    int Gx[3][3] = {{-1, 0, 1} ,{-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1} ,{0, 0, 0}, {1, 2, 1}};
    
    typedef struct{
        int rgbtRed;
        int rgbtGreen;
        int rgbtBlue;
    }mytype;
    
    mytype newimage[height][width];
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float sumRedGx = 0;
            float sumGreenGx = 0;
            float sumBlueGx = 0;
            float sumRedGy = 0;
            float sumGreenGy = 0;
            float sumBlueGy = 0;
            
            for (int a = -1; a < 2; a++)
            {
                for (int b = -1; b < 2; b++)
                {
                    if (i + a >= 0 && i + a < height && j + b >= 0 && j + b < width)
                    {
                        sumRedGx += (Gx[a+1][b+1] * image[i+a][j+b].rgbtRed);
                        sumGreenGx += (Gx[a+1][b+1] * image[i+a][j+b].rgbtGreen);
                        sumBlueGx += (Gx[a+1][b+1] * image[i+a][j+b].rgbtBlue);
                        
                        sumRedGy += (Gy[a+1][b+1] * image[i+a][j+b].rgbtRed);
                        sumGreenGy += (Gy[a+1][b+1] * image[i+a][j+b].rgbtGreen);
                        sumBlueGy += (Gy[a+1][b+1] * image[i+a][j+b].rgbtBlue);
                    }
                }
            }
            newimage[i][j].rgbtRed = round(sqrt((sumRedGx * sumRedGx) + (sumRedGy * sumRedGy)));
            if (newimage[i][j].rgbtRed > 255)
            {
                newimage[i][j].rgbtRed = 255;
            }
            
            newimage[i][j].rgbtGreen = round(sqrt((sumGreenGx * sumGreenGx) + (sumGreenGy * sumGreenGy)));
            if (newimage[i][j].rgbtGreen > 255)
            {
                newimage[i][j].rgbtGreen = 255;
            }
            
            newimage[i][j].rgbtBlue = round(sqrt((sumBlueGx * sumBlueGx) + (sumBlueGy * sumBlueGy)));
            if (newimage[i][j].rgbtBlue > 255)
            {
                newimage[i][j].rgbtBlue = 255;
            }
        }
    }
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = newimage[i][j].rgbtRed;
            image[i][j].rgbtBlue = newimage[i][j].rgbtBlue;
            image[i][j].rgbtGreen = newimage[i][j].rgbtGreen;
        }
    }
    return;
}
