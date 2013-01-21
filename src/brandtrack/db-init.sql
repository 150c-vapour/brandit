CREATE TABLE if not exists users
                     (login text, password text, timestamp integer, metainf text);
CREATE TABLE if not exists brands
                     (name text, searchkeys text, searchfreq integer, timestamp integer, metainf text);
CREATE TABLE if not exists brandmentions
                     (id text, sub text, post text, user text, timestamp integer, metainf text);
CREATE TABLE if not exists posttracking
                     (id text, timestamp integer, score integer, ups integer, downs integer);
CREATE TABLE if not exists ignoresubs
                     (name text);


INSERT INTO brands VALUES('yum!','taco bell', 0, 0, '');
INSERT INTO brands VALUES('yum!','kfc', 0, 0, '');
INSERT INTO brands VALUES('yum!','pizza hut', 0, 0, '');
INSERT INTO brands VALUES('coke','mountain dew', 0, 0, '');
INSERT INTO brands VALUES('coke','fanta', 0, 0, '');
INSERT INTO brands VALUES('coke','sprite', 0, 0, '');
INSERT INTO brands VALUES('coke','cherry coke', 0, 0, '');
INSERT INTO brands VALUES('coke','coke classic', 0, 0, '');
INSERT INTO brands VALUES('coke','mtn dew', 0, 0, '');
INSERT INTO brands VALUES('burger king','burger king', 0, 0, '');
INSERT INTO brands VALUES('doritos','doritos', 0, 0, '');
INSERT INTO brands VALUES('red bull','red bull', 0, 0, '');

INSERT INTO ignoresubs VALUES('/r/RandomActsOfPizza/');
INSERT INTO ignoresubs VALUES('/r/Random_Acts_Of_Pizza/');
INSERT INTO ignoresubs VALUES('/r/tacobell/');
INSERT INTO ignoresubs VALUES('/r/fastfood/');
INSERT INTO ignoresubs VALUES('/r/cocacola/');
INSERT INTO ignoresubs VALUES('/r/HailCorporate/');
