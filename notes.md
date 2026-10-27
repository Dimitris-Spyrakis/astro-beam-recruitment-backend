##### **Part 1**



###### What I implemented

&#x20;I wanted to implement both ENUM and TEXT variables

for the user.role and the observations.status viewing

both enums and constraint ideas.



###### Cause of confusion

&#x20;The confusing bit was that once you create an enum

it is "stored" and re-running the code creates errors

kinda like creating a table that already exists



###### Sources for solution

&#x20;For the problem solving I searched quite a lot of cases

where people had similar problems, combining that with

the PostgreSQL documentation I managed to do this task despite

this being my first experience with PSQL.



###### **Concerning .fits**



I think using file pointers is much faster than searching the whole

BLOB for the wanted data.





##### **Part 2**



###### What I implemented

&#x20;I implemented the FastAPI backend and connected it the Supabase server via psycopg3.

Based on the restpoints the user can either view existing observations, search a specific

observation based on its UUID or even create a new one within a certain frequency range.



###### Cause of confusion

&#x20;The whole part was a new experience for me and a deep dive into many new subjects

I had to learn how everything works from the start including FastAPI, restpoint usage

and finally learning to combine all that with the psycopg3 syntax. I also saw an implementaion

that created a eg "CreateObservation" class using pydantic and using that in the main.py to

create a new Observation object, though I was rather confused on the "how" this could be applied

so I insert data using purely cursor executions with PostgreSQL commmands.

&#x20;

###### Sources for solution

&#x20;The answer to my problems came through a lot of Internet searching in forums, such as

StackOverflow, Youtube, the documentation of needed services; Pydantic,psycopg etc and

the discussion of alternative code implementations with fellow programmers.

&#x20;

&#x20;I think the clean part about my implementaion is getting handled by the psycopg3 module 

itself. With the Supabase connection string as the only input parameter the process becomes

rather simple yet directed.

&#x20;I saw many ways to structure validation errors, specifically 3, and I implemented all of them.

The parameters inputed by the user (at post/observations) are checked within the main.py using

HTTPExteptions, but the validation also happens within the schema.py where the class "Observations"

itself accepts only objects of a certain frequency range. I also saw an alternative where a method

is implemented within the "Observations" class but I think the other two validation checks already 

work things out.

