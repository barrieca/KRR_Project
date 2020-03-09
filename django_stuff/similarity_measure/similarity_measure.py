def main():
    witcher = {
        'gameName': ('Witcher 3'),
        'artist': ('Marian_Chomiak',),
        'designer': ('Grzegorz_Mocarski',),
        'developmentStudio': ('CD_Projekt_RED',),
        'releaseYear': (2015,),
        'score': (93,),
        'videoGameGenre': ('Action_role-playing_game',)
    }
    nhl = {
        'gameName': ('NHL 17'),
        'developmentStudio': ('EA_Canada',),
        'releaseYear': (2016,),
        'score': (79,),
        'videoGameGenre': ('Sports_game',)
    }
    witcher_dlc = {
        'gameName': 'Witcher 3: Blood and Wine',
        'composer': ('Marcin_Przybylowicz',),
        'developmentStudio': ('CD_Projekt_RED',),
        'director': ('Konrad_Tomaszkiewicz',),
        'programmer': ('Grzegorz_Mocarski',),
        'releaseYear': (2016,),
        'videoGameGenre': ('Action_role-playing_game',),
        'writer': ('Marcin_Blacha', 'Mateusz_Tomaszkiewicz', 'Pawel_Sasko')
    }
    warhammer = {
        'gameName': 'Warhammer 40,000',
        'developmentStudio': ('Behaviour_Interactive',),
        'releaseYear': (2016,),
        'videoGameGenre': ('Massively_multiplayer_online_game',)
    }
    oxenfree = {
        'gameName': 'Oxenfree',
        'composer': ('Scntfc',),
        'designer': ('Kevin_Riach',),
        'designer': ('Spencer_Stuard',),
        'developmentStudio': ('Night_School_Studio',),
        'director': ('Adam_Hines',),
        'programmer': ('Bryant_Cannon',),
        'releaseYear': (2016,),
        'videoGameGenre': ('Adventure_game', 'Coming-of-age_story', 'Supernatural_fiction'),
        'writer': ('Marcin_Blacha', 'Mateusz_Tomaszkiewicz', 'Pawel_Sasko')
    }
    darksouls = {
        'gameName': 'Dark Souls III',
        'composer': ('Motoi_Sakuraba',),
        'designer': ('Hiroshi_Yoshida',),
        'designer': ('Junya_Ishizaki',),
        'designer': ('Shigeto_Hirai',),
        'designer': ('Yuya_Kimijima',),
        'developmentStudio': ('FromSoftware',),
        'director': ('Hidetaka_Miyazaki',),
        'programmer': ('Takeshi_Suzuki',),
        'releaseYear': (2012,),
        'videoGameGenre': ('Action_role-playing_game',),
    }
    print(find_similar_games({
        'composer': 1,
        'artist': 1,
        'designer': 1,
        'director': 1,
        'developmentStudio': 1,
        'writer': 1,
        'score': 1,
        'releaseYear': 1,
        'videoGameGenre': 1,
        'programmer': 1
    }, [(witcher,('releaseYear','videoGameGenre')), (nhl, 'writer')], [[witcher_dlc, warhammer, oxenfree, darksouls, nhl],
                        [warhammer, witcher, oxenfree, darksouls]]))

def find_similar_games(similarity_dict, list_of_player_games, list_of_candidate_game_lists):
    '''
    Returns a list of three games most similar to the list of games the player listed, given a list of candidates
        provided by the analogy function from Companions
    :param similarity_dict: proxy similarity vector (contains weight for each attribute)
    :param list_of_player_games: list of games user said they liked
    :param list_of_candidate_game_lists: list of list of candidates provided by analogy function from Companions
    :return: list of three games most similar to player_games, with their corresponding score dictionaries
    '''

    def dew_it(list_of_player_games, list_of_candidate_game_lists):
        '''
        Prints 'Dew it.' and does it.
        :param list_of_player_games: list_of_player_games: list of tuples containing the dictionary of a game the user
            said they liked and one or more attributes for aspects the user liked about that game
        :param list_of_candidate_game_lists: list_of_candidate_game_lists: list of list of candidates provided by
            analogy function from Companions
        :return: list of three games most similar to player_games, with their corresponding score dictionaries
        '''
        print('Dew it.')
        return similarity_measure(list_of_player_games, list_of_candidate_game_lists)

    def similarity_measure(list_of_player_games, list_of_candidate_game_lists):
        '''
        For each game and each corresponding list of candidate games, finds similarity scores (and vectors), aggregates
            the scores in dictionaries, and sorts the scored games
        :param list_of_player_games: list of games user said they liked
        :param list_of_candidate_game_lists: list_of_candidate_game_lists: list of list of candidates provided by
            analogy function from Companions
        :return: list of three games most similar to player_games, with their corresponding score dictionaries
        '''
        list_of_candidate_lists = []
        if not list_of_candidate_game_lists:
            return 0
        for i in range(len(list_of_player_games)):
            if len(list_of_candidate_game_lists) > i:
                list_of_candidate_lists.append([(candidate_game['gameName'], similarity_score(list_of_player_games[i], candidate_game))
                                                for candidate_game in list_of_candidate_game_lists[i]])
        candidate_dict = {}
        for li in list_of_candidate_lists:
            li.sort(key=lambda x: x[1][0], reverse=True)
        for candidate_list in list_of_candidate_lists:
            for i in range(len(candidate_list)):
                if candidate_list[i][0] in candidate_dict:
                    candidate_dict[candidate_list[i][0]] = (candidate_dict[candidate_list[i][0]][0]+
                                                            candidate_list[i][1][0]/(i+1),
                                                            candidate_dict[candidate_list[i][0]][1])
                else:
                    candidate_dict[candidate_list[i][0]] = candidate_list[i][1][0]/(i+1), candidate_list[i][1][1]
        final_recommended_games_list = []
        for k, v in candidate_dict.items():
            final_recommended_games_list.append((k, v))
        final_recommended_games_list = sorted(final_recommended_games_list, key=lambda x: x[1][0], reverse=True)
        return [(t[0], t[1][1]) for t in final_recommended_games_list][:3]

    def similarity_score(player_game, candidate_game):
        '''
        Creates the score vector and finds how many similarities the candidate game has with the player game
        :param player_game: game user said they liked
        :param candidate_game: candidate game provided by analogy in Companions
        :return: returns a similarity score and its corresponding score dictionary
        '''
        candidate_game_score = {
            'composer': 0,
            'programmer': 0,
            'artist': 0,
            'designer': 0,
            'director': 0,
            'developmentStudio': 0,
            'writer': 0,
            'score': 0,
            'releaseYear': 0,
            'videoGameGenre': 0
        }
        for k, v in player_game[0].items():
            if k == 'gameName':
                continue
            if k == 'videoGameSystem':
                continue
            if k in candidate_game:
                if type(v[0]) == int:
                    player_value = v[0]
                    candidate_value = candidate_game[k][0]
                    if player_value > 1000:
                        candidate_game_score['releaseYear'] += similar_year(player_value, candidate_value)
                    elif player_value <= 1000:
                        candidate_game_score['score'] += similar_score(player_value, candidate_value)
                else:
                    get_possible_combinations(k, v, candidate_game[k], candidate_game_score)
        if type(player_game[1]) == tuple:
            print(player_game)
            for attribute in player_game[1]:
                candidate_game_score[attribute] *= 2
        return pseudo_dot_product(candidate_game_score), candidate_game_score

    def pseudo_dot_product(candidate_game_score):
        '''
        Does a dot product between candidate game scores and similarity score
        :param candidate_game_score:
        :return: scalar dot product
        '''
        return sum(candidate_game_score[k]*similarity_dict[k] for k, v in candidate_game_score.items())

    def similar_score(player_score, candidate_score):
        '''
        Checks if difference between scores less than or equal to 5
        :param player_score:
        :param candidate_score:
        :return:
        '''
        return abs(player_score-candidate_score) <= 5

    def similar_year(player_year, candidate_year):
        '''
        Checks if difference between release years less than or equal to 2
        :param player_year:
        :param candidate_year:
        :return:
        '''
        return abs(player_year-candidate_year) <= 2

    def get_possible_combinations(key, player_value, candidate_value, candidate_score_dict):
        '''
        Checks all common values in candidate value and player value
        :param key:
        :param player_value:
        :param candidate_value:
        :param candidate_score_dict:
        :return:
        '''
        if type(player_value) == tuple:
            if type(candidate_value) == tuple:
                candidate_score_dict[key] += sum(x == y for x in player_value for y in candidate_value)
            else:
                candidate_score_dict[key] += sum([candidate_value == x for x in player_value])
        elif type(candidate_value) == tuple:
            candidate_score_dict[key] += sum([player_value == x for x in candidate_value])
        else:
            candidate_score_dict[key] += player_value == candidate_value
        return candidate_score_dict

    return dew_it(list_of_player_games, list_of_candidate_game_lists)

main()
