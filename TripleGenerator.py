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
            triples.append(('director', row.g[0], d))

        for p in row.programmer:
            triples.append(('programmer', row.g[0], p))

        for a in row.artist:
            triples.append(('artist', row.g[0], a))

        for c in row.composer:
            triples.append(('composer', row.g[0], c))

        for w in row.writer:
            triples.append(('writer', row.g[0], w))

        for d in row.designer:
            triples.append(('designer', row.g[0], d))

        for g in row.genre:
            triples.append(('genre', row.g[0], g))

        for d in row.developer:
            triples.append(('developer', row.g[0], d))

        for d in row.release_date:
            triples.append(('release_date', row.g[0], d))

        for s in row.score:
            triples.append(('score', row.g[0], s))

        return triples

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

        # 2b. Convert names containing spaces to have underscores (e.g. Makoto Sonoyama > Makoto_Sonoyama)
        for col in columns:
            df[col] = df[col].str.strip()
            df[col] = df[col].str.replace(' ', '_')

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
            'score': []
        })

        # 1. Collect the data from the all the csv's
        for csv in input_paths:
            # Read in the csv file
            df_temp = pd.read_csv(csv)

            # Format the dataframe values properly
            df_temp = self.__format_dataframe_strings(df_temp)

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
                                              'score': ' '.join}).reset_index()

        # Remove empty values
        columns = list(df_games)
        for col in columns:
            df_games[col] = df_games[col].str.strip()

        # Remove duplicate values and store all entries in the dataframe as a list
        df_games = df_games.applymap(lambda x: list(set(x.split())))

        return df_games


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
