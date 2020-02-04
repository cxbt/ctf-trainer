DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS challenge;
DROP TABLE IF EXISTS records;
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  isAdmin BOOL NOT NULL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  email TEXT NOT NULL,
  score INTEGER NOT NULL
);
CREATE TABLE challenge (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  thumbsup INTEGER NOT NULL,
  flag TEXT NOT NULL,
  score INTEGER NOT NULL
);
CREATE TABLE records (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  userid INTEGER NOT NULL,
  challengeid INTEGER NOT NULL,
  FOREIGN KEY(userid) REFERENCES user(id),
  FOREIGN KEY(challengeid) REFERENCES challenge(id)
);
INSERT INTO user (username, password, isAdmin, email, score)
VALUES
  (
    'test',
    'pbkdf2:sha256:150000$RFWE75Ir$76366beffd12322efb7eb52b913b671c969abfdfb91607d405129728b05e4838',
    0,
    'test@test.com',
    0
  ),
  (
    'lowte',
    'pbkdf2:sha256:150000$td2GOrSN$a17ce2468a922a26d07dddd7590d9a00dc33bb6a004035a74198c08623a9a576',
    1,
    'lowte@gmail.com',
    0
  ),
  (
    'jblee',
    'pbkdf2:sha256:150000$4DcoEeaV$581b8a6fd8cb4ac473d74be847f48ab2d0438f9fec4f727241f10c4a3dce555c',
    0,
    'jblee@teruten.com'
    0
  ),
  (
    'blackkey',
    'pbkdf2:sha256:150000$8klHkIjE$49dba58a381a5b21dca846314377e64e988b3137418382a1552219b9dc49ef35'
    0,
    'suninatas@gmail.com',
    0
  ),
  (
    'meme',
    'pbkdf2:sha256:150000$4A00Ap0a$cc380af3e34430d099cf13a25f059d389da62d022902d8307ad3faf686d2cf55',
    0,
    'meme@meme.com',
    0
  );
INSERT INTO challenge (title, body, thumbsup, flag, score)
VALUES
  (
    'Mic Check',
    'Long time no see little fella, are you ready for a new round? 
    
LOWTE{m1c_ch3cK}',
    0,
    'pbkdf2:sha256:150000$G8CzwElb$c959685cbbce97301933cb7fca20778aa43a01aef502eecf1c2476eb2d76b8af',
    1
  );
INSERT INTO challenge (title, body, thumbsup, flag, score)
VALUES
  (
    'In code',
    'How many encoding method do you know? Can you decode below text?

9M\_h7=0;6F^JW8DKK5t0kYWLAR@-62d^cB1itT^0lC>c0LR^F',
    0,
    'pbkdf2:sha256:150000$iJTAPf0N$895bc99c33986aa4629eefd477e9f9f8e63d8ef62841224973441e549003a1e5',
    10
  );