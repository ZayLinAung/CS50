// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <strings.h>
#include <string.h>
#include <ctype.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned long N = 10000;

// Hash table
node *table[N];
int word_counter = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int code = hash(word);
    node *cursor = table[code];
    while(cursor != NULL)
    {
        if(strcasecmp(cursor->word, word) == 0 )
        {
            return true;
        }
        cursor = cursor -> next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    //referenced from https://stackoverflow.com/questions/64699597/how-to-write-djb2-hashing-function-in-c
    unsigned long hash = 5381;
    int c;

    while ((c = *word++))       
    {
        if (isupper(c))
        {
            c = c + 32;
        }

        hash = ((hash << 5) + hash) + c; 
    }

    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *dic = fopen (dictionary, "r");
    if (dic == NULL)
    {
        printf("Could not open the file.\n");
        return false;
    }
    char tmpword[LENGTH + 1];
    while (fscanf(dic, "%s" , tmpword) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        strcpy (n->word, tmpword);
        int index = hash(n->word);
        n->next = table[index];
        table[index] = n;
        word_counter++;
    }
    fclose(dic);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return word_counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            cursor = cursor-> next;
            free(table[i]);
            table[i]= cursor;
        }
    }
    return true;
}
