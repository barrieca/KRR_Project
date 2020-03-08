import pandas as pd
import unidecode # pip install Unidecode
import re
import os

class TripleGenerator:
    def __init__(self):
        pass

    def generate_entity_instances(self, path_to_triples, path_to_output_file):
        '''
        Generates additional triples that define the entity instances used in the originally generated triples.
        :param path_to_original_triples: A path to the triples to create entity instances for.
        :param path_to_output_file: A path to the file where the newly generated triples will be stored.
        :return: None
        ToDo:
            Add to include functionality for category
        '''
        with open(path_to_triples, encoding="utf8") as f:
            list_of_lines = f.readlines()
        fw = open(path_to_output_file, "w+", encoding="utf8")

        # Get all unique instances of entities that we have data on
        genre_set = set()
        person_set = set()
        programmer_set = set()
        artist_set = set()
        composer_set = set()
        writer_set = set()
        director_set = set()
        designer_set = set()
        game_set = set()
        developer_set = set()
        video_game_system_set = set()

        for line in list_of_lines:
            tup = eval(line)
            if tup[0] == "videoGameGenre":
                genre_set.add(tup[2])
            elif tup[0] == "programmer":
                programmer_set.add(tup[2])
                person_set.add(tup[2])
            elif tup[0] == "artist":
                artist_set.add(tup[2])
                person_set.add(tup[2])
            elif tup[0] == "composer":
                composer_set.add(tup[2])
                person_set.add(tup[2])
            elif tup[0] == "writer":
                writer_set.add(tup[2])
                person_set.add(tup[2])
            elif tup[0] == "director":
                director_set.add(tup[2])
                person_set.add(tup[2])
            elif tup[0] == "designer":
                designer_set.add(tup[2])
                person_set.add(tup[2])
            elif tup[0] == "developmentStudio":
                developer_set.add(tup[2])
                person_set.add(tup[2])
            elif tup[0] == "videoGameSystem":
                video_game_system_set.add(tup[2])
            elif len(tup) > 2 and tup[2] == "VideoGame":
                game_set.add(tup[1])

        # Generate the triples instantiating the entities
        for g in genre_set:
            try:
                fw.write(str(('isa', g, 'VideoGameGenre')) + '\n')
            except UnicodeEncodeError:
                print(g)
        for p in programmer_set:
            try:
                fw.write(str(('isa', p, 'Programmer')) + '\n')
            except UnicodeEncodeError:
                print(p)
        for p in artist_set:
            try:
                fw.write(str(('isa', p, 'Artist')) + '\n')
            except UnicodeEncodeError:
                print(p)
        for p in writer_set:
            try:
                fw.write(str(('isa', p, 'Writer')) + '\n')
            except UnicodeEncodeError:
                print(p)
        for p in composer_set:
            try:
                fw.write(str(('isa', p, 'Composer')) + '\n')
            except UnicodeEncodeError:
                print(p)
        for p in director_set:
            try:
                fw.write(str(('isa', p, 'Director')) + '\n')
            except UnicodeEncodeError:
                print(p)
        for p in designer_set:
            try:
                fw.write(str(('isa', p, 'Designer')) + '\n')
            except UnicodeEncodeError:
                print(p)
        for p in person_set:
            try:
                fw.write(str(('isa', p, 'Person')) + '\n')
            except UnicodeEncodeError:
                print(p)
        for p in game_set:
            try:
                fw.write(str(('isa', p, 'VideoGame')) + '\n')
            except UnicodeEncodeError:
                print(p)
        for p in developer_set:
            try:
                fw.write(str(('isa', p, 'DevelopmentStudio')) + '\n')
            except UnicodeEncodeError:
                print(p)
        for p in video_game_system_set:
            try:
                fw.write(str(('isa', p, 'VideoGameSystem')) + '\n')
            except UnicodeEncodeError:
                print(p)
        fw.close()

    def __convert_row_to_triples(self, row):
        '''
        Converts a single row containing all information about a video game to the proper lisp-style triples.
        :param row: Row containing all relevant data about a single video game.
        :return: A list of lisp-style triples.
        '''

        triples = []

        triples.append(('in-microtheory', row.g[0] + 'Mt'))
        triples.append(('isa', row.g[0], 'VideoGame'))

        for d in row.director:
            sub_entities = self.__extract_entities_from_comma_list(d)
            for se in sub_entities:
                triples.append(('director', row.g[0], se))

        for p in row.programmer:
            sub_entities = self.__extract_entities_from_comma_list(p)
            for se in sub_entities:
                triples.append(('programmer', row.g[0], se))

        for a in row.artist:
            sub_entities = self.__extract_entities_from_comma_list(a)
            for se in sub_entities:
                triples.append(('artist', row.g[0], se))

        for c in row.composer:
            sub_entities = self.__extract_entities_from_comma_list(c)
            for se in sub_entities:
                triples.append(('composer', row.g[0], se))

        for w in row.writer:
            sub_entities = self.__extract_entities_from_comma_list(w)
            for se in sub_entities:
                triples.append(('writer', row.g[0], se))

        for d in row.designer:
            sub_entities = self.__extract_entities_from_comma_list(d)
            for se in sub_entities:
                triples.append(('designer', row.g[0], se))

        for g in row.genre:
            sub_entities = self.__extract_entities_from_comma_list(g)
            for se in sub_entities:
                triples.append(('videoGameGenre', row.g[0], se))

        for d in row.developer:
            sub_entities = self.__extract_entities_from_comma_list(d)
            for se in sub_entities:
                triples.append(('developmentStudio', row.g[0], se))

        # Add the most recent release year for the game
        most_recent_release_year = self.__get_recent_release_year(row.release_date)
        if most_recent_release_year is not None:
            triples.append(('releaseYear', row.g[0], str(most_recent_release_year)))

        # Add the highest review score for the game
        highest_score = self.__get_highest_review_score(row.score)
        if highest_score is not None:
            triples.append(('score', row.g[0], str(highest_score)))

        for p in row.platform:
            sub_entities = self.__extract_entities_from_comma_list(p)
            for se in sub_entities:
                triples.append(('videoGameSystem', row.g[0], se))

        return triples

    def __extract_entities_from_comma_list(self, s):
        '''
        Extracts the individual entities in the given string.
        :param s: A string containing entities separated by commas or other special characters.
        :return: List of entities in the string
        '''
        initial_entities = s.split(',')

        entities = []
        for e in initial_entities:
            entities.extend(e.split('&'))

        entities = [e.strip('_') for e in entities]
        entities = [e for e in entities if e != '']

        return entities

    def __get_highest_review_score(self, row_scores):
        '''
        Returns an integer representing the highest score in the dataframe cell of scores.
        :param scores: The cell of a dataframe containing strings with scores.
        :return: The highest score as an integer.
        Note: These scores can be strings containing ints, floats, or scores pre-pended with platforms (i.e.
        'XONE:_72/100')
        '''
        score_strings = [s for s in row_scores]
        score_strings = [s.replace('/100', '') for s in score_strings]
        score_strings = [s.replace('X360', '') for s in score_strings]

        new_score_strings = []
        for s in score_strings:
            sub_strings = s.split('_')
            for ss in sub_strings:
                new_score_strings.extend(re.findall(r'\d+', ss))

        scores = [int(float(s)) for s in new_score_strings]

        return max(scores) if len(scores) > 0 else None

    def __get_recent_release_year(self, row_dates):
        '''
        Returns an integer representing the most recent release year in the dataframe cell of dates.
        :param row_dates: The cell of a dataframe containing strings with dates in YYYY-MM-DD format.
        :return: The most recent release year as an integer.
        '''
        date_strings = [s for s in row_dates]

        new_date_strings = []
        for s in date_strings:
            sub_strings = s.split('-')
            for ss in sub_strings:
                new_date_strings.extend(re.findall(r'\d+', ss))

        years = [int(float(s)) for s in new_date_strings]

        return max(years) if len(years) > 0 else None

    def __format_dataframe_strings(self, df):
        '''
        Formats the values/strings present in the dataframe to the proper format.
        :param df: A Pandas dataframe of values to format.
        :return: A properly formatted Pandas dataframe.
        '''

        # Replace all NaNs with empty string
        df = df.replace(pd.np.nan, '', regex=True)

        # 1. Convert any numbers present into strings
        df['score'] = df['score'].astype(str)

        # 2. Format the strings in the columns properly
        # 2a. Remove http://dbpedia.org/resource/
        columns = list(df)
        for col in columns:
            df[col] = df[col].str.replace('http://dbpedia.org/resource/', '')
            df[col] = df[col].str.replace('http://dbpedia.org/property/', '')
            df[col] = df[col].str.replace('http://dbpedia.org/ontology/', '')
            df[col] = df[col].str.replace(r'[(]\d*_*\S*[)]', r'')
            df[col] = df[col].str.strip('_')

        # 2b. Convert names containing spaces to have underscores (e.g. Makoto Sonoyama > Makoto_Sonoyama)
        for col in columns:
            df[col] = df[col].str.strip()
            df[col] = df[col].str.replace(' ', '_')
            df[col] = df[col].str.replace('\"', '')
            df[col] = df[col].str.replace(':', '')
            df[col] = df[col].str.replace('.', '')
            df[col] = df[col].str.replace('/', '')

        # 3. Convert any game names that have commas in them to have an underscore instead
        df['g'] = df['g'].str.replace(',', '')
        df['g'] = df['g'].str.replace(':', '')
        df['g'] = df['g'].str.replace(';', '_')

        # 4. Remove URLs from (development studios) columns
        df['developer'].mask(df['developer'].str[0:4] == 'http', '', inplace=True)

        return df

    def __create_dataframe_from_csv(self, input_paths):
        '''
        Generates a Pandas dataframe of the games in the list of input csv's.
        :param input_paths: List of filepaths to the csv files to convert to triples.
        :return: A dataframe that is clean and in the proper format for generating triples.
        '''

        # Initialize the master dataframe that will collect all data for the triple output file.
        df_games = pd.DataFrame({
            'g': [],
            'director': [],
            'programmer': [],
            'artist': [],
            'composer': [],
            'writer': [],
            'designer': [],
            'genre': [],
            'developer': [],
            'release_date': [],
            'score': [],
            'platform': []
        })

        # 1. Collect the data from the all the csv's
        for csv in input_paths:
            # Read in the csv file
            df_temp = pd.read_csv(csv)

            # Format the dataframe values properly
            df_temp = self.__format_dataframe_strings(df_temp)

            # Add platform column to the dataframe
            platform = os.path.basename(csv)
            platform = platform.split('_')[0]
            df_temp['platform'] = platform

            # Add in the newest set of csv values into the global dataframe of games
            df_games = df_games.append(df_temp, ignore_index=True)

        # 2. Combine rows with same game name
        # https://stackoverflow.com/questions/36271413/pandas-merge-nearly-duplicate-rows-based-on-column-value
        df_games = df_games.groupby('g').agg({'director': ' '.join,
                                              'programmer': ' '.join,
                                              'artist': ' '.join,
                                              'composer': ' '.join,
                                              'writer': ' '.join,
                                              'designer': ' '.join,
                                              'genre': ' '.join,
                                              'developer': ' '.join,
                                              'release_date': ' '.join,
                                              'score': ' '.join,
                                              'platform': ' '.join}).reset_index()

        # Remove empty values
        columns = list(df_games)
        for col in columns:
            df_games[col] = df_games[col].str.strip()

        # Remove duplicate values and store all entries in the dataframe as a list
        df_games = df_games.applymap(lambda x: list(set(x.split())))

        return df_games

    def generate_list_of_game_names(self, path_to_triples, path_to_output_file='data/game_list.csv'):
        '''
        Writes a csv to data containing a nicely formatted list of games present in our data.
        :param path_to_triples:
        :return:
        '''
        with open(path_to_triples, encoding="utf8") as f:
            list_of_lines = f.readlines()
        out_f = open(path_to_output_file, "w+", encoding="utf8")

        # Write out the header line for the csv
        out_f.write('game_symbol, game_name\n')

        for line in list_of_lines:
            tup = eval(line)
            if tup[0] == "isa" and tup[2] == 'VideoGame':
                game_name = tup[1]

                # Clean up the game name
                nice_game_name = re.sub(r'[(]\d*_*video_game[)]', r'', game_name)
                nice_game_name = nice_game_name.replace('_', ' ')
                nice_game_name = nice_game_name.strip()

                try:
                    out_f.write(game_name + ', ' + nice_game_name + '\n')
                except UnicodeEncodeError:
                    print(game_name)

        out_f.close()

    def create_triples_from_csv(self, input_paths, output_path):
        '''
        Generates a single file of lisp style triples from a list of csv files.
        :param input_path: File path to the csv file to convert to triples.
        :param output_path: File path to the text file where the new triples will be stored.
        :return: None
        '''

        # Generate a dataframe for the given list of csv files
        df_games = self.__create_dataframe_from_csv(input_paths)

        # 3. Write out each row (which should contain one game each) to a triples file
        # - Make this a separate function which takes a game name, a lists of the various properties to represent,
        # and the output file.
        # - May want to make this a member function of a Game Object, if we need more operations to be defined, or to
        # make it more modular. Would be useful when joining information from multiple sources. Or maybe just use
        # multiple dataframes and combine them that way first... more thought needed in the future.

        # Open and overwrite a file
        with open(output_path, 'w+') as f:
            for row in df_games.itertuples():
                triples = self.__convert_row_to_triples(row)
                for t in triples:
                    f.write(str(t) + '\n')

        print("Converted csv to triples. Results stored in " + output_path)

        return

    def clean_csv(self, path_to_csv):
        '''
        Cleans the csv. Currently removes accented characters.
        :param path_to_csv: File path to the csv to clean.
        :return: None
        '''
        # Open the file
        f = open(path_to_csv, 'r+')
        s = f.read()

        # Perform the cleaning
        s = self.__remove_accented_characters(s)
        s = s.replace('*', '')
        s = s.replace('\'', '')

        # Overwrite the file with the new string
        f.seek(0)
        f.truncate()
        f.write(s)
        f.close()

    def __remove_accented_characters(self, string):
        '''
        Deaccents any specials characters in the given string.
        :param string: A string to deaccent.
        :return: The deaccented string.
        '''
        return unidecode.unidecode(string)

    def generate_triples_krf(self, path_to_triples_txt, path_to_output_file, microtheory='VideoGamesMt'):
        '''
        Generates a properly formatted krf file with triples in the given microtheory.
        :param path_to_triples_txt: The filepath to a text file of triples in the format: ('pred' 'arg1' 'arg2'),
                                    i.e. tuples of strings
        :param path_to_output_file: The filepath to the krf file.
        :param microtheory: The microtheory in which the triples will be added in the krf file.
        :return: None
        '''
        # Read in the triples text file
        with open(path_to_triples_txt, encoding="utf8") as f:
            list_of_lines = f.readlines()

        # Create a new output file for this krf or overwrite the old one
        out_f = open(path_to_output_file, "w+", encoding="utf8")

        # Write out the microtheory line plus a newline char
        out_f.write('(in-microtheory ' + microtheory + ')\n\n')

        # Convert each line to a string output, and write it to the file
        for line in list_of_lines:
            tup = eval(line)
            try:
                if len(tup) == 3:
                    out_f.write('(' + tup[0] + ' '+ tup[1] + ' ' + tup[2] + ')\n')
                elif len(tup) == 2:
                    out_f.write('(' + tup[0] + ' ' + tup[1] + ')\n')
            except UnicodeEncodeError:
                print(line)

        out_f.close()

        print('Finished converting .txt to .krf')

        return

    def generate_case_library_krf(self, path_to_output_file, path_to_games='data/game_list.csv'):
        '''
        Creates the case library needed for the performing analogical reasoning in Companions.
        :param path_to_output_file: Path to the output file.
        :param path_to_games: The list of games with which to generate the case library.
        :return: None
        '''
        fw = open(path_to_output_file, 'w+')
        r = 0
        with open(path_to_games) as f:
            fw.write('(in-microtheory VideoGamesMt)\n\n')
            fw.write('(isa VideoGameCaseLibrary CaseLibrary)\n\n')

            for row in f:
                if r == 0:
                    r += 1
                else:
                    fw.write('(caseLibraryContains VideoGameCaseLibrary '+row.split()[0][:-1]+'Mt)\n')
        fw.close()
