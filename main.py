import TripleGenerator as tg


def main():
    # Instantiate the triple generator
    generator = tg.TripleGenerator()

    # Specify the csv files from which the data will be gathered
    csv_files = ['data/PS4_games_1.csv','data/PS4_games_2.csv','data/PS4_games_3.csv','data/PS4_games_4.csv',
                 'data/PC_games_2000-2004_1.csv', 'data/PC_games_2005-2008_1.csv', 'data/PC_games_2005-2008_2.csv', 'data/PC_games_2009-2012_1.csv',
                 'data/PC_games_2009-2012_2.csv', 'data/PC_games_2009-2012_3.csv', 'data/PC_games_2013-2016_1.csv', 'data/PC_games_2013-2016_2.csv',
                 'data/PC_games_2013-2016_3.csv', 'data/PC_games_2017-2020_1.csv', 'data/PC_games_no_date_1.csv', 'data/PC_games_no_date_2.csv',
                 'data/PC_games_pre_2000_1.csv', 'data/PC_games_pre_2000_2.csv', 'data/SWITCH_games_1.csv', 'data/WII_U_games_1.csv',
                 'data/XONE_games_1.csv', 'data/XONE_games_2.csv', 'data/XONE_games_3.csv', 'data/XONE_games_4.csv', 'data/XONE_games_5.csv',
                 'data/XONE_games_6.csv', 'data/XONE_games_7.csv']

    # Clean the data in these csv files
    for csv in csv_files:
        generator.clean_csv(csv)

    # Generate the triples text files
    generator.create_triples_from_csv(csv_files, 'data/triples.txt')
    generator.generate_entity_instances('data/triples.txt', 'data/instance_triples.txt')

    # Generate a file that maps from the name of the game entity to a nicely formatted string version for use in the UI
    generator.generate_list_of_game_names('data/instance_triples.txt', 'data/game_list.csv')

    # Convert the triples text files to krf files
    generator.generate_triples_krf('data/triples.txt', 'knowledge/Video_Game_Triples.krf')
    generator.generate_triples_krf('data/instance_triples.txt', 'knowledge/Video_Game_Instance_Triples.krf')

    generator.generate_case_library_krf('knowledge/Video_Game_Case_Library.krf')

if __name__ == "__main__":
    main()
