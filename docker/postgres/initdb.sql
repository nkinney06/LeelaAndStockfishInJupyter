CREATE TABLE games (
	game SERIAL PRIMARY KEY,
	white VARCHAR(31),
	black VARCHAR(31),
	result VARCHAR(15),
        time INTEGER,
	stamp TIMESTAMP NOT NULL DEFAULT NOW(),
	moves TEXT
	);

CREATE TABLE matches (
	match SERIAL PRIMARY KEY,
	white VARCHAR(31),
	black VARCHAR(31),
	games INTEGER,
        dep INTEGER,
	whiteBookMoves INTEGER,
	blackBookMoves INTEGER,
	score INTEGER,
	percent FLOAT,
	stamp TIMESTAMP NOT NULL DEFAULT NOW()
	);


