DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS movie_review;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE movie_review (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  movie_name TEXT NOT NULL,
  actors TEXT NOT NULL,
  director TEXT NOT NULL,
  length INTEGER NOT NULL, -- TODO Check how add limit and label next to it
  genre TEXT NOT NULL,
  rating INTEGER NOT NULL, -- TODO Check how add limit and label next to it
  review TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
