# self-blog-bot

A discord bot providing a feature of blogs-for-anyone at a server


Currently, one client supports only one guild

> You may contact me for free hosting of your bot based on my code - if the project still alive there won't be any problem for me

#### The way bot works:

- Administrator creates a channel1 with some rules of blogs (perhaps)
	- Bot sends a message in the channel1 with a button to create a new blog
- The process of creation takes its place in DM with the bot
	- User provides the title and description for his brand new blog
	- Anyone is allowed to create only one blog
	- Users can change their blog's info once a day
- Administrator sets up a channel2 for moderation of blogs
	- Before creating any blog bot will ask the moderation whether the blog is good or not
- Administrator creates a channel3 where the presentation cards of blogs will be posted
	- After changing a blog's info by its creator the presentation card will be re-posted
	- Every presentation card has a button allowing other users to follow the blog
	- No one has to be approved by blog's owner before accessing it :yellow_circle: *I've decided that it's OK to make blogs completely open to follow* :yellow_circle:
- Bot creates its own category for text channels where the blogs will take their place
	- In the text channel of a blog the owner has to post directly - after each message the bot creates a discussion where anyone can comment :yellow_circle: *perhaps, in future the owner will be able to turn off the comments in his/her blog* :yellow_circle:


Thanks for your attention! Feel free to contact me with any questions and considerations
