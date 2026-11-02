## **Part 1**



&emsp;First I opened a Supabase server and in the SQL editor I created 2 scripts one for creating the necessary tables and one for inserting some test values or ,via selections, checking the contents of my tables each time. I wanted to implement both ENUM and TEXT variables for the user.role and the observations.status.  
The two tables have ID as their primary key while the "observations" table has a direct dependency on the user_id such the FOREIGN KEY constraint.  
I then created an enum for role giving a "role" type attribute to the "users" table while for the observations I used the CONSTRAINED mechanism. Both of these implementations required little internet searching but still challenged me a bit to understand how they work and why the compiler kept showing me erros. Although overwhelming due to my first contact with PostgreSQL and the Supabase server I found a lot of material online from people having similar issues as me so I managed to fit it all together at the end.



### Concerning .fits

If I understand the structure of .fits files correctly then I think that the header before each data section is a much faster and easier way of finding specific data through the whole file. While BLOBs can fit a lot of data, managing through it seems much more difficult.



## Part 2



&emsp;This was one of the most challenging bits of the whole task. I had to do a deep dive into what everything is and how it works. It required a lot of digging into Internet forums, some YouTube videos and the modules' documentations to really see how everything is structured. Once I had an idea of each components work (Pydantic, FastAPI, psycopg) I had to "merge" them together while making sure my code stays clean and readable.  
I then started to implement the restpoints, though I saw many people defining the required functions with "async". I think this is not a big of an issue now since the functionality of the API is very simple and not many processes run at the same time (if I understand the concept of synchronous vs asynchronous functions correctly). I started with implementing each restpoint with some dummy values and once I got the logic down I then procceeded with the psycopg3 syntax.  
One of the challenges was learning tuples again and how to insert, update and fetch values within them (a bit more difficult when we have a tuple within a tuple!) but having guidance from my fellow programmer friends I grasped the concept pretty quickly. This was important to learn because in my first implementation I used dictionaries to store values, but since psycopg3 returns tuples from the executed queries I had to adapt to it.  
The logic behind each restpoint is not complicated. After I set the connection I pass the parameter into my functions then simply executing a query that fetches me the information that I want (e.g return all observations). The tricky bit was passing arguments into the query string. I raised some HTTPException messages where problems would occur so the user can have an understanding of why the server encountered said error.   
I think the most significant part of this code is the assignment of unique IDS when posting an observation. If I was writing purely in SQL the parameter would be handled completely by the UNIQUE constraint so I would have no problem Inserting or Deleting data, but since I am implementing this in python I had to find a way to fetch the current maximum ID within the observations database and simply adding 1 to create another unique id.



### Connection and Validation solutions

&emsp;I think the clean part about my implementation is getting handled by the psycopg3 module itself. With the Supabase connection string as the only input parameter the process becomes rather simple yet directed.
 I saw many ways to structure validation errors, specifically 3, and I implemented all of them . The parameters inputed by the user (at post/observations) are checked within the main.py usingmHTTPExteptions, but the validation also happens within the schema.py where the class "Observations" itself accepts only objects of a certain frequency range. I also saw an alternative where a method is implemented within the "Observations" class but I think the other two validation checks already work things out.



## Part 3



&emsp;In a new script I implemented the autonomous worker that works around using two functions. One fetches the ID of the oldest pending observation or processing (if the program stops with no pending observations left) and the other uses the ID to update the specific observation's status. Through the process each required timestamp is updated  and the according URI is attached to each completed observation. It was difficult to understand how everything will work together and I still haven't fully built it because I couldn't implement the router logic. I used some Internet resources, though it was very limited and tried to mimic the implementation of Part 2. With the help of my collagues I was also able to tackle down some specific exceptions and run-time problems polishing my code as much as I could.



### Concurrency Issues

&emsp;If some data happen to arrive at the exact same time then we would have a problem: 

* the timestamp is exactly the same and 
* which observation should get the "new ID value"? 

I think the answer lies to the Isolation mechanism which manages how readers and writers view or block each other based on 5 different levels.


