import TripleGenerator as tg

def main():
    generator = tg.TripleGenerator()
    generator.create_triples_from_csv('data/playstation_4_game_data.csv', 'data/triples.txt')


if __name__ == "__main__":
    main()
