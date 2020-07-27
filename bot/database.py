import sqlite3

class Database:
    db_file = ""
    def __init__(self, db_file):
        self.db_file = db_file

    def create_tables(self):
        with sqlite3.connect(self.db_file) as conn:
            query = """
            CREATE TABLE IF NOT EXISTS play_requests(
            id              INTEGER PRIMARY KEY,
            video_title     VARCHAR(128),
            video_link      VARCHAR(1024),
            member_id       INT,
            guild_id        INT,
            datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);"""
            conn.execute(query)

    def add_play_request(self, video_title, video_link, member_id, guild_id):
        with sqlite3.connect(self.db_file) as conn:
            query = """
                    INSERT INTO play_requests(video_title, video_link, member_id, guild_id) values (?, ?, ?, ?)
                    """
            conn.execute(query, (video_title, video_link, member_id, guild_id))



if __name__ == '__main__':
    db = Database('data.db')
    db.create_tables()
    db.add_play_request("deneme", "https://www.youtube.com/watch?v=ai05A1l1t-I", 13130)