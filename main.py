import TripleGenerator as tg


def main():
    # Instantiate the triple generator
    generator = tg.TripleGenerator()

    # Specify the csv files from which the data will be gathered
    csv_files = ['data/PS4_games_1.csv','data/PS4_games_2.csv','data/PS4_games_3.csv','data/PS4_games_4.csv']

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
