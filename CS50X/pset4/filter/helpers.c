#include "helpers.h"
#include <math.h>

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

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0 ; j < width; j++)
        {
            int sepiaRed =  round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            int sepiaGreen = round(.349 *image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;            
            }
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
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

RGBTRIPLE newimage[height][width];


    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int divider = 0;
            int sumRed = 0;
            int sumGreen = 0;
            int sumBlue = 0;
            for (int a = -1; a < 2; a++)
            {
                for (int b = -1; b < 2; b++)
                {
                    if ((j + b >= 0 && j + b < width) && (i + a >= 0 && i + a < height))
                    {
                        sumRed += image[i+a][j+b].rgbtRed;
                        sumGreen += image[i+a][j+b].rgbtGreen;
                        sumBlue += image[i+a][j+b].rgbtBlue;
                        divider++;
                    }
                }
            }
            newimage[i][j].rgbtRed = round((sumRed) / (float)divider);
            newimage[i][j].rgbtGreen = round((sumGreen) / (float)divider);
            newimage[i][j].rgbtBlue = round((sumBlue) / (float)divider);
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
}

