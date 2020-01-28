DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS challenge;
DROP TABLE IF EXISTS record;
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  isAdmin BOOL NOT NULL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  email TEXT NOT NULL
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
CREATE TABLE record (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TIMESTAMP NOT NULL,
  solved BOOL NOT NULL,
  user_id INTEGER NOT NULL,
  challenge_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (challenge_id) REFERENCES challenge (id)
);
INSERT INTO user (username, password, isAdmin, email)
VALUES
  (
    'test',
    'pbkdf2:sha256:150000$RFWE75Ir$76366beffd12322efb7eb52b913b671c969abfdfb91607d405129728b05e4838',
    0,
    'maumau@maumau.com'
  ),
  (
    'lowte',
    'pbkdf2:sha256:150000$td2GOrSN$a17ce2468a922a26d07dddd7590d9a00dc33bb6a004035a74198c08623a9a576',
    1,
    'lowte@gmail.com'
  );
INSERT INTO challenge (title, body, thumbsup, flag, score)
VALUES
  (
    'Mic Check',
    'Long time no see little fella, are you ready for a new round? LOWTE{m1c_ch3cK}',
    0,
    'pbkdf2:sha256:150000$G8CzwElb$c959685cbbce97301933cb7fca20778aa43a01aef502eecf1c2476eb2d76b8af',
    1
  )