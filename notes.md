## **Part 1**



First I opened a Supabase server and in the SQL editor I created 2 scripts one for creating the necessary tables and one for inserting some test values or ,via selections, checking the contents of my tables each time. I wanted to implement both ENUM and TEXT variables for the user.role and the observations.status. The two tables have ID as their primary key while the "observations" table has a direct dependency on the user\_id such the FOREIGN KEY constraint. I then created an enum for role giving a "role" type attribute to the "users" table while for the observations I used the CONSTRAINED mechanism. Both of these implementations required little internet searching but still challenged me a bit to understand how they work and why the compiler kept showing me erros. Although overwhelming due to my first contact with PostgreSQL and the Supabase server I found a lot of material online from people having similar issues as me so I managed to fit it all together at the end.



### Concerning .fits

If I understand the structure of .fits files correctly then I think that the header before each data section is a much faster and easier way of finding specific data through the whole file. While BLOBs can fit a lot of data, managing through it seems much more difficult.



## Part 2



This was one of the most challenging bits of the whole task. I had to do a deep dive into what everything is and how it works. It required a lot of digging into Internet forums, some YouTube videos and the modules' documentations to really see how everything is structured. Once I had an idea of each components work (Pydantic, FastAPI, psycopg) I had to "merge" them together while making sure my code stays clean and readable. I then started to implement the restpoints, though I saw many people defining the required functions with "async". I think this is not a big of an issue now since the functionality of the API is very simple and not many processes run at the same time (if I understand the concept of synchronous vs asynchronous functions correctly). I started with implementing each restpoint with some dummy values and once I got the logic down I then procceeded with the psycopg3 syntax.
One of the challenges was learning tuples again and how to insert, update and fetch values within them (a bit more difficult when we have a tuple within a tuple!) but having guidance from my fellow programmer friends I grasped the concept pretty quickly. This was important to learn because in my first implementation I used dictionaries to store values, but since psycopg3 returns tuples from the executed queries I had to adapt to it. The logic behind each restpoint is not complicated. After I set the connection I pass the parameter into my functions then simply executing a query that fetches me the information that I want (e.g return all observations). The tricky bit was passing arguments into the query string. I raised some HTTPException messages where problems would occur so the user can have an understanding of why the server encountered said error.  I think the most significant part of this code is the assignment of unique IDS when posting an observation. If I was writing purely in SQL the parameter would be handled completely by the UNIQUE constraint so I would have no problem Inserting or Deleting data, but since I am implementing this in python I had to find a way to fetch the current maximum ID within the observations database and simply adding 1 to create another unique ID.



### Connection and Validation solutions

I think the clean part about my implementation is getting handled by the psycopg3 module itself. With the Supabase connection string as the only input parameter the process becomes rather simple yet directed.
I saw many ways to structure validation errors, specifically 3, and I implemented all of them. The parameters inputed by the user (at post/observations) are checked within the **main.py** using HTTPExteptions, but the validation also happens within the **schema.py** where the class *"Observations"* itself accepts only objects of a certain frequency range. I also saw an alternative where a method is implemented within the "Observations" class but I think the other two validation checks already work things out.



## Part 3



In a new script I implemented the autonomous worker that works around using two functions. One fetches the ID of the oldest pending observation or processing (if the program stops with no pending observations left) and the other uses the ID to update the specific observation's status. Through the process each required timestamp is updated  and the according URI is attached to each completed observation. It was difficult to understand how everything will work together and I still haven't fully built it because I couldn't implement the router logic. I used some Internet resources, though it was very limited and tried to mimic the implementation of Part 2. With the help of my collagues I was also able to tackle down some specific exceptions and run-time problems polishing my code as much as I could.



### Concurrency Issues

 If some data happen to arrive at the exact same time then we would have a problem:

1. The timestamp is exactly the same.
2. Which observation should get the "new ID value"?

I think the answer lies to the Isolation mechanism which manages how readers and writers view or block each other based on 5 different levels.



## Part 4



In this part I tried to implement the mock email notification once an observation has reached it's "Completed" status since I thought it would be very helpful for the observations' users to receive a directed message for the results of each request.

Since each person has their own busy schedule, automating things could help keep everything organized without having to constantly, for example, check the webpage itself from time to time, worrying of forgetting it.

This could cause more stress than needed. An email is a very common way of getting notified nowadays, so simply checking one's phone is enough to keep them updated at any given time and day while they are parralelly working on other subjects.

The way I approached this was by building an *EmailSchema* class, a *ConfigConnection* item and a background function for sending emails all in the **telescope\_poller.py**.

The reason for this was that I wanted the email function to be called from the *polling\_oldest\_obs\_comp* function so that the changing of status and email-sending are both done simutaneously.

I changed the function's hint to bool, so the email function can know if the status change was succesfull or not. Although I thought my approach would work I run into some issues in the code that I wasn't able to resolve:

First I saw that many people online implemented the email-sending notification as a "post" restpoint which would require for the admin to manually type the email of each user requesting an observation and I think that counters the automation process I am trying to implement.

The other problem was within the *send\_in\_background* function when I tried to create a *MessageSchema* type object. The usual way I saw this being approached was to set the recipients as "recipients=email.dict().get("email")". However VS Code had a problem with the *dict()* function (~~dict~~()) so I tried to change it to "recipients=email.model\_dump().get("email")", after looking at it online but I still couldn't get it to work.

I don't know in general if implementing the email functions and classes inside the **telescope\_poller.py** was the best approach, because it also affects **Part 3**'s code functionality, but I think this was the simplest way of approaching this without complicating it further.



## Part 5

