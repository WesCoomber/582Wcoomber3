# Yolo paper template
```bash
make          # for quite mode
make loud     # for error 
make tidy     # for submisssion
make clean    # git mode
make spell    # ispell check 
make view     # build & open the pdf
```

For spelling check in vim, use `:set spell`
```
To search for the next misspelled word:

]s           Move to next misspelled word after the cursor.
             A count before the command can be used to repeat.
             'wrapscan' applies.

[s           Like "]s" but search backwards, find the misspelled
             word before the cursor.  

Finding suggestions for bad words:

z=           For the word under/after the cursor, suggest correctly
             spelled words.

To add words to your own word list:

zg           Add word under the cursor as a good word
```
