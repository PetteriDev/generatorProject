CREATE TABLE cramo_generators (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    run_id INTEGER NOT NULL,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    photo_url TEXT
);

CREATE TABLE ramirent_generators (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    run_id INTEGER NOT NULL,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    photo_url TEXT
);

CREATE SEQUENCE scrape_run_id_seq START 1;
