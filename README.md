# tarotbot
A Discord chatbot that does tarot spreads.

## Acknowledgments
Images in /imgsrc obtained from http://www.m31.de/colman-smith/index.html under the General Public license

Three-word upright and inverted descriptions obtained from https://labyrinthos.co/blogs/tarot-card-meanings-list under fair use

## To use
You can add this bot to your servers with [this link.](https://discordapp.com/oauth2/authorize?client_id=659747523354689549&scope=bot&permissions=100352)

Commands have the prefix "t!". This bot supports the following commands:

`1card` A one card spread.

`3card` A three-card spread.

`5card` A five-card spread.

`celtic` A Celtic Cross spread.

By default, spreads are sent as an image of randomly selected cards accompanied by brief text descriptions of the cards.

Each command takes the following optional flags:

`--t` Text-only spread.

`--n` Disable inverted cards.

`--e` Send unembedded response.

`--i` Image-only spread.

For example, `t!3card --e --i` will generate an unembedded image of a three-card spread.

![ex](https://66.media.tumblr.com/5bd515de2d2d93593d3037083e91a9e1/5a17c53fecdeae20-b0/s1280x1920/56549989be54a9c524cc235beef182d467faef92.png)
![ex](https://66.media.tumblr.com/e8c5e38414f3e35bcc8ca94f35926d79/5a17c53fecdeae20-dc/s1280x1920/32023695d72429036b3073c76384252e1c77dd6e.png)
