import requests
from bs4 import BeautifulSoup
import time
import global_variables as my_var
def find_my_team(item, last_pos):
    my_temp = item.find('span class', item.find('/team/view/', last_pos))
    my_test_temp = item.find('home', my_temp, my_temp + 30)
    if my_test_temp > 0:
        return my_temp + 18
    else:
        return my_temp + 14


def find_my_live_stats(item, last_pos):
    goal_list = []
    while True:
        image_home_pos_home = item.find('<img src="/img/home_goal.png"/>', last_pos)
        image_home_pos_away = item.find('<img src="/img/away_goal.png"/>', last_pos)
        if image_home_pos_home==-1:
            if image_home_pos_away!=-1:
                image_home_pos_home_away = image_home_pos_away
                scored_goal_by = 'Away'
            else:
                break
        else:
            if image_home_pos_away!=-1:
                if image_home_pos_home < image_home_pos_away:
                    image_home_pos_home_away = image_home_pos_home
                    scored_goal_by = 'Home'

                else:
                    image_home_pos_home_away = image_home_pos_away
                    scored_goal_by = 'Away'
            else:
                image_home_pos_home_away = image_home_pos_home
                scored_goal_by = 'Home'

        pos_goal_time_start = item.find('left', image_home_pos_home_away - 30) + 5
        pos_goal_time_end = item.find('%', pos_goal_time_start)
        goal_time = item[pos_goal_time_start: pos_goal_time_end]

        goal_list.append((scored_goal_by, round((int(goal_time)/100)*90)))

        last_pos = pos_goal_time_end + 31
    return goal_list

def get_my_team_first_page_link(my_league_link):
    # print(my_league_link)
    time.sleep(1)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(my_league_link, headers=headers)
        response.raise_for_status()

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        table_soup = soup.find('table')
        my_list_with_soup_elements = []
        for row in table_soup.findAll("tr"):
            my_list_with_soup_elements.append(str(row))
            # print(row)
            # print("--------------------------------")
        counter = 0
        my_table=[]
        for item in my_list_with_soup_elements:


            pos_match_id_start = item.find('data-match_id=') + 15
            pos_match_id_end = item.find('<td class=', pos_match_id_start) - 3

            pos_league_start = item.find('target="_blank">',item.find('/league/view',pos_match_id_end)) + 16
            pos_league_end = item.find('</a>', pos_league_start)

            pos_date_time_start = item.find('<td class="text-center">',pos_league_end) + 24
            pos_date_time_end = item.find('</td>', pos_date_time_start)

            pos_team_home_start = find_my_team(item, pos_date_time_end)
            pos_team_home_end = item.find('</span>', pos_team_home_start)

            pos_goal_start = item.find('match_goal', pos_team_home_end) + 12
            pos_goal_end = item.find('</td>', pos_goal_start)

            pos_team_away_start = find_my_team(item, pos_goal_end)
            pos_team_away_end = item.find('</span>', pos_team_away_start)

            pos_corner_start = item.find('span_match_corner', pos_team_away_end) + 19
            pos_corner_end = item.find('</span>', pos_corner_start)

            pos_half_corner_start = item.find('span_half_corne', pos_corner_end) + 19
            pos_half_corner_end = item.find('</span>', pos_half_corner_start) - 1

            pos_dangerous_attacks_start = item.find('match_dangerous_attacks_div', pos_half_corner_end) + 29
            pos_dangerous_attacks_end = item.find('</div>', pos_dangerous_attacks_start)

            pos_shots_start = item.find('match_shoot_div', pos_dangerous_attacks_end) + 17
            pos_shots_end = item.find('</div>', pos_shots_start)

            if pos_goal_end -  pos_goal_start <10 and 8<pos_match_id_end - pos_match_id_start <12:

                match_id = item[pos_match_id_start:pos_match_id_end]
                league = item[pos_league_start:pos_league_end]
                date_time = item[pos_date_time_start:pos_date_time_end]
                team_home = item[pos_team_home_start:pos_team_home_end]
                goal = item[pos_goal_start:pos_goal_end]
                team_away = item[pos_team_away_start:pos_team_away_end]
                corner = item[pos_corner_start:pos_corner_end]
                half_corner = item[pos_half_corner_start:pos_half_corner_end]
                dangerous_attacks = item[pos_dangerous_attacks_start:pos_dangerous_attacks_end]
                shots = item[pos_shots_start:pos_shots_end]

                # ================================         LIVE            ===========================

                live_stats_goals = find_my_live_stats(item, pos_shots_end)
                # print(pos_match_id_end - pos_match_id_start)
                my_table.append((match_id,league,date_time,team_home,goal,team_away,corner,half_corner,dangerous_attacks,shots,live_stats_goals))

                # print(match_id)
                # print(league)
                # print(date_time)
                # print(team_home)
                # print(goal)
                # print(team_away)
                # print(corner)
                # print(half_corner)
                # print(dangerous_attacks)
                # print(shots)
                # print(live_stats_goals)
                # print("--------------------------------", counter)

                counter = counter + 1

        return my_table
    except Exception as error:
        print("sdfgasdf")
        print(type(error))
        print(error.args)
        time.sleep(10)
        print(error)
        if my_var.my_old_url != my_league_link:
            my_var.my_counter=5
        while my_var.my_counter>0:

            time.sleep(5)
            my_var.my_counter = my_var.my_counter - 1
            my_var.my_old_url = my_league_link
            get_my_team_first_page_link(my_league_link)




