import sqlite3
import pandas as pd
import numpy as np


def get_teams_data(team1, team2):
    global my_team1, my_team2
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # sql = f"""SELECT * FROM table_goals
    #         JOIN table_team_games ON table_goals.Game_ID = table_team_games.Game_ID
    #     """

    sql_team1 = f"""SELECT *  FROM table_team_games as t1
            JOIN table_goals as t2 ON t1.Game_ID = t2.Game_ID 
            WHERE t1.Home='{team1}' OR t1.Away='{team1}' 
        """
    sql_team2 = f"""SELECT *  FROM table_team_games as t1
            JOIN table_goals as t2 ON t1.Game_ID = t2.Game_ID 
            WHERE t1.Home='{team2}' OR t1.Away='{team2}' 
        """

    my_team1 = c.execute(sql_team1).fetchall()
    my_team2 = c.execute(sql_team2).fetchall()

    conn.commit()
    conn.close()


def create_excel_detail():
    global my_team1, my_team2
    try:
        table1 = pd.DataFrame(my_team1)
        table2 = pd.DataFrame(my_team2)

        # Add an identifier column to distinguish the tables
        table1['Table'] = 'Table1'
        table2['Table'] = 'Table2'

        table1.columns = ['ID','Game_ID','League','Date','Home','Goal_Home','Goal_Away','Away','Corner','Half_corner','Attacks',
                          'Shots','ID_goals','Game_ID','Minutes','Home_Away','table']
        table2.columns = ['ID','Game_ID','League','Date','Home','Goal_Home','Goal_Away','Away','Corner','Half_corner','Attacks',
                          'Shots','ID_goals','Game_ID','Minutes','Home_Away','table']
        # Combine the tables one below the other, aligning columns by name
        combined_table = pd.concat([table1, table2], axis=0, ignore_index=True, sort=False)

        # Save the combined table to an Excel file
        file_path = 'C:/Users/AlexPc/Desktop/combined_table.xlsx'
        combined_table.to_excel(file_path, index=False)
    except Exception as error:
        print(error.args)


def find_goals_per_15minutes(team1, team2):
    global my_team1, my_team2

    def initialize_goal_lists():
        return [[0] * 8 for _ in range(4)]
    # print(team1, "   ", team2)
    my_team1_score_goals_home, my_team1_score_goals_away, my_team2_score_goals_home, my_team2_score_goals_away = initialize_goal_lists()
    my_team1_get_goals_home, my_team1_get_goals_away, my_team2_get_goals_home, my_team2_get_goals_away = initialize_goal_lists()

    for i in my_team1:
        # print(i)
        if i[4] == team1:
            if i[15] == 'Home':
                if int(i[14]) <= 15:
                    my_team1_score_goals_home[0] = my_team1_score_goals_home[0] + 1
                elif int(i[14]) <= 30:
                    my_team1_score_goals_home[1] = my_team1_score_goals_home[1] + 1
                elif int(i[14]) <= 45:
                    my_team1_score_goals_home[2] = my_team1_score_goals_home[2] + 1
                elif int(i[14]) <= 60:
                    my_team1_score_goals_home[3] = my_team1_score_goals_home[3] + 1
                elif int(i[14]) <= 75:
                    my_team1_score_goals_home[4] = my_team1_score_goals_home[4] + 1
                else:
                    my_team1_score_goals_home[5] = my_team1_score_goals_home[5] + 1
                my_team1_score_goals_home[6] = my_team1_score_goals_home[6] + 1
                if int(i[14]) >= 85:
                    my_team1_score_goals_home[7] = my_team1_score_goals_home[7] + 1
            else:
                if int(i[14]) <= 15:
                    my_team1_get_goals_home[0] = my_team1_get_goals_home[0] + 1
                elif int(i[14]) <= 30:
                    my_team1_get_goals_home[1] = my_team1_get_goals_home[1] + 1
                elif int(i[14]) <= 45:
                    my_team1_get_goals_home[2] = my_team1_get_goals_home[2] + 1
                elif int(i[14]) <= 60:
                    my_team1_get_goals_home[3] = my_team1_get_goals_home[3] + 1
                elif int(i[14]) <= 75:
                    my_team1_get_goals_home[4] = my_team1_get_goals_home[4] + 1
                else:
                    my_team1_get_goals_home[5] = my_team1_get_goals_home[5] + 1
                my_team1_get_goals_home[6] = my_team1_get_goals_home[6] + 1
                if int(i[14]) >= 85:
                    my_team1_get_goals_home[7] = my_team1_get_goals_home[7] + 1

        if i[7] == team1:
            if i[15] == 'Away':
                if int(i[14]) <= 15:
                    my_team1_score_goals_away[0] = my_team1_score_goals_away[0] + 1
                elif int(i[14]) <= 30:
                    my_team1_score_goals_away[1] = my_team1_score_goals_away[1] + 1
                elif int(i[14]) <= 45:
                    my_team1_score_goals_away[2] = my_team1_score_goals_away[2] + 1
                elif int(i[14]) <= 60:
                    my_team1_score_goals_away[3] = my_team1_score_goals_away[3] + 1
                elif int(i[14]) <= 75:
                    my_team1_score_goals_away[4] = my_team1_score_goals_away[4] + 1
                else:
                    my_team1_score_goals_away[5] = my_team1_score_goals_away[5] + 1
                my_team1_score_goals_away[6] = my_team1_score_goals_away[6] + 1
                if int(i[14]) >= 85:
                    my_team1_score_goals_away[7] = my_team1_score_goals_away[7] + 1
            else:
                if int(i[14]) <= 15:
                    my_team1_get_goals_away[0] = my_team1_get_goals_away[0] + 1
                elif int(i[14]) <= 30:
                    my_team1_get_goals_away[1] = my_team1_get_goals_away[1] + 1
                elif int(i[14]) <= 45:
                    my_team1_get_goals_away[2] = my_team1_get_goals_away[2] + 1
                elif int(i[14]) <= 60:
                    my_team1_get_goals_away[3] = my_team1_get_goals_away[3] + 1
                elif int(i[14]) <= 75:
                    my_team1_get_goals_away[4] = my_team1_get_goals_away[4] + 1
                else:
                    my_team1_get_goals_away[5] = my_team1_get_goals_away[5] + 1
                my_team1_get_goals_away[6] = my_team1_get_goals_away[6] + 1
                if int(i[14]) >= 85:
                    my_team1_get_goals_away[7] = my_team1_get_goals_away[7] + 1
    for i in my_team2:
        if i[4] == team2:
            if i[15] == 'Home':
                if int(i[14]) <= 15:
                    my_team2_score_goals_home[0] = my_team2_score_goals_home[0] + 1
                elif int(i[14]) <= 30:
                    my_team2_score_goals_home[1] = my_team2_score_goals_home[1] + 1
                elif int(i[14]) <= 45:
                    my_team2_score_goals_home[2] = my_team2_score_goals_home[2] + 1
                elif int(i[14]) <= 60:
                    my_team2_score_goals_home[3] = my_team2_score_goals_home[3] + 1
                elif int(i[14]) <= 75:
                    my_team2_score_goals_home[4] = my_team2_score_goals_home[4] + 1
                else:
                    my_team2_score_goals_home[5] = my_team2_score_goals_home[5] + 1
                my_team2_score_goals_home[6] = my_team2_score_goals_home[6] + 1
                if int(i[14]) >= 85:
                    my_team2_score_goals_home[7] = my_team2_score_goals_home[7] + 1
            else:
                if int(i[14]) <= 15:
                    my_team2_get_goals_home[0] = my_team2_get_goals_home[0] + 1
                elif int(i[14]) <= 30:
                    my_team2_get_goals_home[1] = my_team2_get_goals_home[1] + 1
                elif int(i[14]) <= 45:
                    my_team2_get_goals_home[2] = my_team2_get_goals_home[2] + 1
                elif int(i[14]) <= 60:
                    my_team2_get_goals_home[3] = my_team2_get_goals_home[3] + 1
                elif int(i[14]) <= 75:
                    my_team2_get_goals_home[4] = my_team2_get_goals_home[4] + 1
                else:
                    my_team2_get_goals_home[5] = my_team2_get_goals_home[5] + 1
                my_team2_get_goals_home[6] = my_team2_get_goals_home[6] + 1
                if int(i[14]) >= 85:
                    my_team2_get_goals_home[7] = my_team2_get_goals_home[7] + 1
        if i[7] == team2:
            if i[15] == 'Away':
                if int(i[14]) <= 15:
                    my_team2_score_goals_away[0] = my_team2_score_goals_away[0] + 1
                elif int(i[14]) <= 30:
                    my_team2_score_goals_away[1] = my_team2_score_goals_away[1] + 1
                elif int(i[14]) <= 45:
                    my_team2_score_goals_away[2] = my_team2_score_goals_away[2] + 1
                elif int(i[14]) <= 60:
                    my_team2_score_goals_away[3] = my_team2_score_goals_away[3] + 1
                elif int(i[14]) <= 75:
                    my_team2_score_goals_away[4] = my_team2_score_goals_away[4] + 1
                else:
                    my_team2_score_goals_away[5] = my_team2_score_goals_away[5] + 1
                my_team2_score_goals_away[6] = my_team2_score_goals_away[6] + 1
                if int(i[14]) >= 85:
                    my_team2_score_goals_away[7] = my_team2_score_goals_away[7] + 1
            else:
                if int(i[14]) <= 15:
                    my_team2_get_goals_away[0] = my_team2_get_goals_away[0] + 1
                elif int(i[14]) <= 30:
                    my_team2_get_goals_away[1] = my_team2_get_goals_away[1] + 1
                elif int(i[14]) <= 45:
                    my_team2_get_goals_away[2] = my_team2_get_goals_away[2] + 1
                elif int(i[14]) <= 60:
                    my_team2_get_goals_away[3] = my_team2_get_goals_away[3] + 1
                elif int(i[14]) <= 75:
                    my_team2_get_goals_away[4] = my_team2_get_goals_away[4] + 1
                else:
                    my_team2_get_goals_away[5] = my_team2_get_goals_away[5] + 1
                my_team2_get_goals_away[6] = my_team2_get_goals_away[6] + 1
                if int(i[14]) >= 85:
                    my_team2_get_goals_away[7] = my_team2_get_goals_away[7] + 1



    print('TOTAL')
    print(f'Team {team1} scored Home:    {my_team1_score_goals_home[:6]}  '
          f'Total goals:{my_team1_score_goals_home[6:7]} / Goals the last 5 min:{my_team1_score_goals_home[7:]}')
    print(f'Team {team1} gets goal Away: {my_team1_get_goals_home[:6]}  '
          f'Total goals:{my_team1_get_goals_home[6:7]} / Goals the last 5 min:{my_team1_get_goals_home[7:]}')
    print("------------------------------------")
    print(f'Team {team1} scored Away:    {my_team1_score_goals_away[:6]}  '
          f'Total goals:{my_team1_score_goals_away[6:7]} / Goals the last 5 min:{my_team1_score_goals_away[7:]}')
    print(f'Team {team1} gets goal Away: {my_team1_get_goals_away[:6]}  '
          f'Total goals:{my_team1_get_goals_away[6:7]} / Goals the last 5 min:{my_team1_get_goals_away[7:]}')
    print("-------------------------------------------------------------")
    print(f'Team {team2} scored Home:    {my_team2_score_goals_home[:6]}  '
          f'Total goals:{my_team2_score_goals_home[6:7]} / Goals the last 5 min:{my_team2_score_goals_home[7:]}')
    print(f'Team {team2} gets goal Home: {my_team2_get_goals_home[:6]}  T'
          f'otal goals:{my_team2_get_goals_home[6:7]} / Goals the last 5 min:{my_team2_get_goals_home[7:]}')
    print("------------------------------------")
    print(f'Team {team2} scored Away:    {my_team2_score_goals_away[:6]}  '
          f'Total goals:{my_team2_score_goals_away[6:7]} / Goals the last 5 min:{my_team2_score_goals_away[7:]}')
    print(f'Team {team2} gets goal Away: {my_team2_get_goals_away[:6]}  '
          f'Total goals:{my_team2_get_goals_away[6:7]} / Goals the last 5 min:{my_team2_get_goals_away[7:]}')

    create_excel_detail()

def start(team1, team2):
    print(team1, "   ", team2)
    global my_team1, my_team2

    get_teams_data(team1, team2)
    find_goals_per_15minutes(team1, team2)


