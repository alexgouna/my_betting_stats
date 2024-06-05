

def list_of_link_to_retreive_data():
    sql = """CREATE TABLE my_links (
                link_id INTEGER NOT NULL,
                link_description text,
                PRIMARY KEY("link_id" AUTOINCREMENT)      
                )"""
    return sql



#CREATE TABLE match
def create_table_match():
    sql = """CREATE TABLE match (
                match_id INTEGER NOT NULL,
                match_team1 text,
                match_team2 text,
                match_team1_goal integer,
                match_team2_goal integer,
                match_team1_corner integer,
                match_team2_corner integer, 
                match_team1_shots integer,
                match_team2_shots integer,            
                match_league text,
                match_league_year integer,
                PRIMARY KEY("match_id" AUTOINCREMENT)              
                )"""
    return sql




