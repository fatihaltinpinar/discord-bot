import psycopg2 as dbapi
import config

class Database:
    db_file = ""
    def __init__(self, db_file):
        self.db_file = db_file

    def create_tables(self):
        with dbapi.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = """
            create table if not exists play_requests(
            id              serial primary key,
            video_title     varchar(128),
            video_link      varchar(1024),
            member_id       varchar(32),
            guild_id        varchar(32),
            datetime timestamp not null default current_timestamp);"""
            query2 = """
            create table if not exists last_match(
            steam_id       varchar(32)  primary key,
            match_id        varchar(32)             
            );
            """
            cursor.execute(query)
            cursor.execute(query2)

    def add_play_request(self, video_title, video_link, member_id, guild_id):
        with dbapi.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = """
                insert into play_requests(video_title, video_link, member_id, guild_id) values (%s, %s, %s, %s)
                    """
            cursor.execute(query, (video_title, video_link, member_id, guild_id))

    def get_member_ids(self, guild_id):
        member_ids = []
        with dbapi.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = """
                select member_id from play_requests where guild_id == %s group by member_id
            """
            cursor.execute(query, (guild_id,))
            for row in cursor:
                member_ids.append(row[0])
        return member_ids

    def get_request_list(self, guild_id):
        request_list = []
        with dbapi.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = """
            select mode() within group ( order by video_title) as video_title,
                   video_link, 
                   count(*) as count,
                   mode() within group ( order by member_id) as member_id 
            from play_requests
            group by video_link
            order by count desc;"""
            cursor.execute(query, (guild_id,))
            request_list = cursor.fetchall()
        return request_list

    def get_top10(self, guild_id):
        request_list = []
        with dbapi.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = """
            select mode() within group ( order by video_title) as video_title,
                   video_link, 
                   count(*) as count,
                   mode() within group ( order by member_id) as member_id 
            from play_requests
            group by video_link
            order by count desc
            limit 10;"""
            cursor.execute(query, (guild_id,))
            request_list = cursor.fetchall()
        return request_list

    def get_last_match(self, steam_id):
        match_id = 0
        with dbapi.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = """
            select match_id from last_match where steam_id == %s;
            """
            cursor.execute(query, (steam_id,))
            match_id = cursor.fetchone()
        return match_id[0]

    def set_last_match(self, steam_id, match_id):
        with dbapi.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = """update last_match set match_id = %s where steam_id == %s;"""
            cursor.execute(query, (match_id, steam_id))
            if cursor.rowcount == 0:
                query = """insert into last_match values (%s, %s);"""
                cursor = conn.execute(query, (steam_id, match_id))



    def get_top10_by_member_id(self, member_id):
        request_list = []
        with dbapi.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = """
            select mode() WITHIN GROUP ( ORDER BY video_title ) as video_title, count(*) as count from play_requests
            where play_requests.member_id = '118406756589109255' 
            group by play_requests.video_link 
            order by count desc limit 10;
            """

            # query = """SELECT video_title, count(*) FROM play_requests
            # where member_id = %s GROUP by video_link ORDER by 2 desc LIMIT 10"""
            cursor.execute(query, (str(member_id),))
            request_list = cursor.fetchall()
        return request_list

if __name__ == '__main__':
    db = Database('data.db')
    db.create_tables()
    print("HELLO")
    print(db.get_last_match(config.OWNER_STEAM_ID))
    print(db.set_last_match(config.OWNER_STEAM_ID, 5537383867))
    print(db.get_last_match(config.OWNER_STEAM_ID))
