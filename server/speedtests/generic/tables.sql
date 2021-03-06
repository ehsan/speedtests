DROP TABLE IF EXISTS generic;
CREATE TABLE generic (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
	browser_id INTEGER REFERENCES browser(id),
	browser_height INTEGER,
	browser_width INTEGER,
	teststart TIMESTAMP,
	ip VARCHAR(128),
	testname VARCHAR(128),
	result_value FLOAT,
	result_data TEXT
);
