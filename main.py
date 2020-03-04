import TripleGenerator as tg


def main():
    generator = tg.TripleGenerator()

    csv_files = ['data/ps4_games_1.csv','data/ps4_games_2.csv','data/ps4_games_3.csv','data/ps4_games_4.csv']

    generator.create_triples_from_csv(csv_files, 'data/triples.txt')


if __name__ == "__main__":
    main()
