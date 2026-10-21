CREATE TYPE role AS ENUM('user','operator','admin');

CREATE TABLE users(
  id INT PRIMARY KEY,
  user_role role
);

CREATE TABLE observations (
  id INT PRIMARY KEY,
  user_id INT,
  center_freq_mhz FLOAT NOT NULL DEFAULT 1420.405,
  status TEXT CONSTRAINT status_check CHECK (status IN ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED')),
  fits_file_url TEXT,
  created_at timestamp,
  started_at timestamp,
  completed_at timestamp,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

--I added some examples for testing
--INSERT INTO users VALUES(1,'admin');
--INSERT INTO users VALUES(2,'user');
--INSERT INTO users VALUES(3,'operator');

--INSERT INTO observations values(1,3,3.567,'PENDING',null,'2012-03-12 13:55:31','2012-04-15 11:50:22','2012-05-02 04:31:53');
--INSERT INTO observations values(2,3,35.267,'COMPLETED',null,'2011-03-12 13:55:31','2012-04-15 11:50:22','2012-05-02 04:31:53');
--INSERT INTO observations values(3,2,5.887,'PENDING',null,'2024-03-12 13:55:31','2024-04-15 11:50:22','2024-05-02 04:31:53');
--INSERT INTO observations values(4,3,43.027,'PENDING',null,'2009-03-12 13:55:31','2010-04-15 11:50:22','2010-05-02 04:31:53');

SELECT * FROM observations
ORDER BY status = 'PENDING' DESC, created_at ASC;--older requests come first!

