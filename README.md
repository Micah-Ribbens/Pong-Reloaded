Finished Development: 05/24/2022

First three years of programming

# Summary
This is a game where there are many different versions of pong. For all but Omnidirectional Pong I developed an AI that
worked nearly every time! Writing the AI code was a fun challenge because it forced me to be able to predict where the ball
would end up and have automated movement. In Omnidirectional Pong, I had a good amount of the logic correct, but I couldn't fit it all
together. I used a state machine to model it, but it was so buggy and complicated I eventually gave up on it. I also used
some complex collision logic. The collision logic would allow me to know the precise moment when two objects collided.
I spent a good amount of a year working on this off and on. This is one of my favorite projects that I worked on.

# Pong Game Modes
- Normal Pong &rarr; The standard game of pong
- Gravity Pong &rarr; Pong except the ball gets acted upon by gravity, so the ball moves in a parabolic motion.
- Middle Paddle Pong &rarr; Pong with a paddle in the middle that moves up and down. This middle paddle can deflect the ball.
- Portal Pong &rarr; Pong with portals! The portals move around the screen and if the ball collides with a portal, the ball teleports to the other end of that same colored portal
- Shatter Pong &rarr; Pong, but with each hit the paddle gets smaller. When the ball hits the paddle, that end of the paddle is removed
- Omnidirectional Pong &rarr; Pong, but four directional movement is possible! Pretty self-explanatory.

# Collision Logic
This was the most complicated collision logic that I developed for a game. With that complexity came a lot of power like
being able to have game objects being incredibly thin and collisions working perfectly. The thinness of game objects change
collisions because in one game tick the other game object could end up passing directly through the other game object.
However, with these complexity came many bugs and float math imprecision eventually made me abandon this methodology. Although
it was quite powerful, it was difficult to get working and collision logic that complex was never needed. The basics of the
collision logic was to see where all the lines of the game object collide with another game object. One line was made for
each corner of the object (a rectangle). The line's start point would be the object's previous position and the line's
end point would be the object's current position. Using all those lines, you can see where the positions of the two object's
overlap. And if the position on the horizontal axis and the position on the vertical axis both have a collision at a certain
time interval, then that is when the object's collide. Overall, a decently intuitive way of doing collisions. The problem,
however, came in with the float math messing up the logic. Floats are not guaranteed to have all their decimals be accurate.
That inaccuracy significantly compounds, especially, when that number is already close to 0. Those inaccuracies could either
mean that a collision is missed, or the collision location is predicted wrongly. This was mostly random, so collisions
could randomly break.

# Bug Fixes 11/27/2023
I did multiple things in order to get this project back into a working condition:
- Changed most of the collision code to a simpler collision system that I have thoroughly tested. This collision code was
my original collisions system before I transitioned to the more complex one. I decided to go back to the simpler one because
it worked better and was less buggy.
- Changed some function calls that were not correct (they crashed the game).
- Made Omnidirectional Pong impossible to play Single Player because the AI in that game crashes the game.