import pandas as pd

class TripleGenerator:
    def __init__(self):
        pass

    def wtf(self):
        '''
        ToDo:
            Convert so it's included in the original parsing
            Add to include functionality for year_released, developer, category
        :return:
        '''
        with open("triples.txt", encoding="utf8") as f:
            list_of_lines = f.readlines()
        fw = open("genres.txt", "w+", encoding="utf8")
        genre_set = set()
        person_set = set()
        programmer_set = set()
        artist_set = set()
        composer_set = set()
        writer_set = set()
        director_set = set()
        designer_set = set()

        for line in list_of_lines:
            tup = eval(line)
            if tup[0] == "genre":
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
        for g in genre_set:
            try:
                fw.write('(isa '+g+' GameGenre)\n')
            except UnicodeEncodeError:
                print(g)
        for p in programmer_set:
            try:
                fw.write('(isa ' + p + ' Programmer)\n')
            except UnicodeEncodeError:
                print(p)
        for p in artist_set:
            try:
                fw.write('(isa ' + p + ' Artist)\n')
            except UnicodeEncodeError:
                print(p)
        for p in writer_set:
            try:
                fw.write('(isa ' + p + ' Writer)\n')
            except UnicodeEncodeError:
                print(p)
        for p in composer_set:
            try:
                fw.write('(isa ' + p + ' Composer)\n')
            except UnicodeEncodeError:
                print(p)
        for p in director_set:
            try:
                fw.write('(isa ' + p + ' Director)\n')
            except UnicodeEncodeError:
                print(p)
        for p in designer_set:
            try:
                fw.write('(isa ' + p + ' Designer)\n')
            except UnicodeEncodeError:
                print(p)
        for p in person_set:
            try:
                fw.write('(isa ' + p + ' Person)\n')
            except UnicodeEncodeError:
                print(p)
        fw.close()

    def __convert_row_to_triples(self, row):
        '''
        Converts a single row containing all information about a video game to the proper lisp-style triples.
        :param row: Row containing all relevant data aobut a single video game.
        :return: A list of lisp-style triples.
        '''

        triples = []

        for d in row.director:
            triples.append(('director', row.game[0], d))

        for p in row.programmer:
            triples.append(('programmer', row.game[0], p))

        for a in row.artist:
            triples.append(('artist', row.game[0], a))

        for c in row.composer:
            triples.append(('composer', row.game[0], c))

        for w in row.writer:
            triples.append(('writer', row.game[0], w))

        for d in row.designer:
            triples.append(('designer', row.game[0], d))

        for g in row.genre:
            triples.append(('genre', row.game[0], g))

        return triples

    def create_triples_from_csv(self, input_path, output_path):
        '''
        Generates lisp style triples from a csv file.
        :param input_path: File path to the csv file to convert to triples.
        :param output_path: File path to the text file where the new triples will be stored.
        :return: None
        '''

        # 0. Read in the csv file
        df_games = pd.read_csv(input_path)
        columns = list(df_games)

        # Replace all NaNs with empty string
        # for col in df_columns:
        #     df_games[col] = df_games[col]
        df_games = df_games.replace(pd.np.nan, '', regex=True)

        # 1. Format the strings in the columns properly
        # 1a. Remove http://dbpedia.org/resource/
        for col in columns:
            df_games[col] = df_games[col].str.replace('http://dbpedia.org/resource/', '')
            df_games[col] = df_games[col].str.replace('http://dbpedia.org/property/', '')
            df_games[col] = df_games[col].str.replace('http://dbpedia.org/ontology/', '')

        # 1b. Convert names containing spaces to have underscores (e.g. Makoto Sonoyama > Makoto_Sonoyama)
        for col in columns:
            df_games[col] = df_games[col].str.replace(' ', '_')


        # 2. Combine similar columns (artist_o artist_p gameArtist_o gameArtist_p > artist)
        # https://stackoverflow.com/questions/19377969/combine-two-columns-of-text-in-dataframe-in-pandas-python
        df_games['game'] = df_games[['g']]
        df_games['director'] = df_games[['director_o', 'director_p']].agg(' '.join, axis=1)
        df_games['programmer'] = df_games[['programmer_o', 'programmer_p']].agg(' '.join, axis=1)
        df_games['artist'] = df_games[['artist_o', 'artist_p', 'gameArtist_o', 'gameArtist_p']].agg(' '.join, axis=1)
        df_games['composer'] = df_games[['composer_o', 'composer_p']].agg(' '.join, axis=1)
        df_games['writer'] = df_games[['writer_o', 'writer_p']].agg(' '.join, axis=1)
        df_games['designer'] = df_games[['designer_o', 'designer_p']].agg(' '.join, axis=1)
        df_games['genre'] = df_games[['genre_o', 'genre_p']].agg(' '.join, axis=1)

        updated_columns = ['game','director','programmer','artist','composer','writer','designer','genre']

        # Remove leading and trailing whitespace
        for col in updated_columns:
            df_games[col] = df_games[col].str.strip()

        # Create a new dataframe with just the data we want to look at
        df_games_new = df_games[updated_columns]

        # 3. Combine rows with same game name
        # https://stackoverflow.com/questions/36271413/pandas-merge-nearly-duplicate-rows-based-on-column-value
        df_games_new = df_games_new.groupby('game').agg({'director': ' '.join,
                                                         'programmer': ' '.join,
                                                         'artist': ' '.join,
                                                         'composer': ' '.join,
                                                         'writer': ' '.join,
                                                         'designer': ' '.join,
                                                         'genre': ' '.join}).reset_index()

        # Remove empty values
        for col in updated_columns:
            df_games_new[col] = df_games_new[col].str.strip()

        # Remove duplicate values and store all entries in the dataframe as a list
        df_games_new = df_games_new.applymap(lambda x: list(set(x.split())))


        # 4. Write out each row (which should contain one game each) to a triples file
        # - Make this a separate function which takes a game name, a lists of the various properties to represent,
        # and the output file.
        # - May want to make this a member function of a Game Object, if we need more operations to be defined, or to
        # make it more modular. Would be useful when joining information from multiple sources. Or maybe just use
        # multiple dataframes and combine them that way first... more thought needed in the future.

        # Open and overwrite a file
        f = open(output_path, 'w+')
        f.truncate()

        with open(output_path, 'w+') as f:
            for row in df_games_new.itertuples():
                triples = self.__convert_row_to_triples(row)
                for t in triples:
                    f.write(str(t) + '\n')

        print("Converted csv to triples. Results stored in " + output_path)

        return
