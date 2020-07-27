import sqlite3

class Database:
    db_file = ""
    def __init__(self, db_file):
        self.db_file = db_file

    def create_tables(self):
        with sqlite3.connect(self.db_file) as conn:
            query = """
            create table if not exists play_requests(
            id              integer primary key,
            video_title     varchar(128),
            video_link      varchar(1024),
            member_id       int,
            guild_id        int,
            datetime timestamp not null default current_timestamp);"""
            conn.execute(query)

    def add_play_request(self, video_title, video_link, member_id, guild_id):
        with sqlite3.connect(self.db_file) as conn:
            query = """
                insert into play_requests(video_title, video_link, member_id, guild_id) values (?, ?, ?, ?)
                    """
            conn.execute(query, (video_title, video_link, member_id, guild_id))

    def get_member_ids(self, guild_id):
        member_ids = []
        with sqlite3.connect(self.db_file) as conn:
            query = """
                select member_id from play_requests where guild_id == ? group by member_id
            """
            cursor = conn.execute(query, (guild_id,))
            for row in cursor:
                member_ids.append(row[0])
        return member_ids

    def get_request_list(self, guild_id):
        request_list = []
        with sqlite3.connect(self.db_file) as conn:
            query = """
            select video_title, video_link, count(id)
            from play_requests
            where guild_id == ? 
            group by video_link 
            order by 3 desc;
            """
            cursor = conn.execute(query, (guild_id,))
            request_list = cursor.fetchall()
        return request_list

if __name__ == '__main__':
    db = Database('data.db')
    db.create_tables()
    db.add_play_request("deneme", "https://www.youtube.com/watch?v=ai05A1l1t-I", 13130)