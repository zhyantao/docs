# 指向结构体的指针

```{code-block} c
#include <stdio.h>
#include <string.h>

struct book_bank
{
    char title[15];
    char author[20];
    int paper;
    float price;
};

struct book_bank *update2(struct book_bank *item)
{
    strcpy(item->title, "Love");
    strcpy(item->author, "Tommy");
    item->paper = 10;
    item->price = 309.9;

    return item;
}

struct book_bank update1(struct book_bank item)
{
    strcpy(item.title, "Love");
    strcpy(item.author, "Tommy");
    item.paper = 10;
    item.price = 309.9;

    return item;
}

int main()
{
    struct book_bank item;
    printf("原始:\t%s\t%s\t%7d\t%13f\n", item.title, item.author, item.paper, item.price);
    update1(item);
    printf("值传递:\t%s\t%s\t%7d\t%13f\n", item.title, item.author, item.paper, item.price);
    update2(&item);
    printf("址传递:\t%s\t%s\t%7d\t%13f\n", item.title, item.author, item.paper, item.price);

    return 0;
}
```
