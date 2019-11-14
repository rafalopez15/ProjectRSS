DROP TABLE IF EXISTS rss;

CREATE TABLE rss (
    rssname TEXT UNIQUE NOT NULL,
    rssurl TEXT NOT NULL,
    rssdate TEXT NOT NULL
);