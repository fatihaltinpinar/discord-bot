import sqlite3
import config

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
            query2 = """
            create table if not exists last_match(
            steam_id       integer primary key,
            match_id        integer             
            );
            """
            conn.execute(query)
            conn.execute(query2)

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
            # query = """
            # select video_title, video_link, count(id)
            # from play_requests
            # where guild_id == ?
            # group by video_link
            # order by 3 desc;
            # """
            query = """
            select video_title, video_link, SUM(request_per_member) as total_requests, member_id from
                (select video_title, video_link, count(*) as request_per_member, member_id from play_requests
                where guild_id = ?
                group by video_link, member_id
                order by video_title, count(*) desc)
            group by video_title
            """
            cursor = conn.execute(query, (guild_id,))
            request_list = cursor.fetchall()
        return request_list

    def get_last_match(self, steam_id):
        match_id = 0
        with sqlite3.connect(self.db_file) as conn:
            query = """
            select match_id from last_match where steam_id == ?;
            """
            cursor = conn.execute(query, (steam_id,))
            match_id = cursor.fetchone()
        return match_id[0]

    def set_last_match(self, steam_id, match_id):
        with sqlite3.connect(self.db_file) as conn:
            query = """update last_match set match_id = ? where steam_id == ?;"""
            cursor = conn.execute(query, (match_id, steam_id))
            if cursor.rowcount == 0:
                query = """insert into last_match values (?, ?);"""
                cursor = conn.execute(query, (steam_id, match_id))




if __name__ == '__main__':
    db = Database('data.db')
    db.create_tables()
    print("HELLO")
    print(db.get_last_match(config.OWNER_STEAM_ID))
    print(db.set_last_match(config.OWNER_STEAM_ID, 5537383867))
    print(db.get_last_match(config.OWNER_STEAM_ID))
