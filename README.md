# RePlay: A Video Game Recommendation System

RePlay is a knowledge based approach for recommending video games. As with all artistic endeavors, the finished 
piece of work is strongly influenced by those who actually work to produce the final product. With this in mind, 
our project aims to allow users to find new video games to play based not only on the genre, rating, and platform, 
but also on the individuals who created the games. To this end, we utilized analogical retrieval and case-based
reasoning techniques to find games with similar creators and artists, and allow for the quality of past recommendations
to enhance future recommendations. This work was done as a final project for CS 371 at Northwestern University.

## Installation

Python Packages required and Python version
Installing Companions
Installing Django

### Running the Project

This section needs to "describes step by step what I will need to do to run your project, anything I need to load,
anything I need to type, and any expected output."

Starting Companions
KRF file loading
Starting Django

### Getting Recommendations

## How Does it Work?

### Knowledge Representation
For this project, we adopted Cyc-style triples, and extended the ontology present within Companions to properly 
represent the entities and properties with which we perform the reasoning.

#### Data Acquisition
To build up a library of video game data, we queried **DBpedia** for a set of video games and their relevant associated
properties. The queries we used can be found in the `queries/` directory. We executed these queries on the DBpedia
SPARQL query endpoint (https://dbpedia.org/sparql).

The video game properties that we queried for are as follows:
- Game Director(s)
- Lead Programmer(s)
- Lead Artist(s)
- Composer(s)
- Writer(s)
- Designer(s)
- Development Studio(s)
- Release Date
- Review Score
- Game System

We collected data for games on PC, PlayStation 4, Xbox One, Nintendo Switch, and Nintendo Wii U. During this process,
there were a number of challenges that needed to be overcome. The first of these challenges was the DBpedia SPARQL query
endpoint imposing a hard limit on the number of rows that could be viewed/downloaded at once, which was capped at 10000.
This problem was relatively simple to overcome by adding an ordering condition (sorted the rows in ascending order 
based on the resource name) and using an offset into the rows (which were set as multiples of 10000).

A second more difficult challenge was that this SPARQL endpoint also limited the *total* number of rows that could be
returned by a single query. This was set to a maximum of 40000 rows. In order to get around this, for platforms that 
have more than 40000 facts associated with them, we incorporate a filter that will filter in and out games that tend 
to have a large number of rows associated with them. This typically includes games with episodic content where each 
of the episodes and its data gets associated with the same base game. This results in two queries that finds games 
and properties for a small set of games, as well as this set's complement.

If there are still too much data for us to query, then a date range was used to query for games within specific date
ranges (or with no dates at all). This was the case for the PC games.

Lastly, the third and most difficult challenge was the problem of sparse data contained in the queryable knowledge base.
There are many games for which a plethora of high quality data is available. This tended to happen for more popular or
highly rated games. Unfortunately, this was a more pernicious issue that we were unable to overcome effectively. 

The end results of this can be found within the `data/` directory. Each query that we ran resulted in a .csv file
for the video game system and its associated data. For almost all of the systems there are multiple csv files. They all
have the same format, but are the separate results from each of the broken up queries.

#### Data Cleaning
All of the data cleaning code can be found within `TripleGenerator.py`. A TripleGenerator object is created
within `main.py`, which takes in a list of csv files which are cleaning and for which triples are generated. 

The first step of the data cleaning pipeline is to remove accented characters, asterisks, and apostrophes from
each of the csv files we are working with. We found that these characters will cause multiple issues throughout
the rest of the pipeline, including issues when loading the final .krf files into Companions.

The next step is to load each csv file into a single Pandas dataframe. This process can be seen in the 
`__create_dataframe_from_csv()` function. Rows with the same URI are combined into a single row, with 
duplicate attribute values removed and attributes with multiple values being stored in a list for that game.

This dataframe is then cleaned further in the `__format_dataframe_strings()` function and the values are formatted 
properly for later conversion to knowledge triples. Within this function, the URI namespaces are removed to leave
just the game name, which is used as the symbol for this entity. Various substrings are removed, including commas, 
colons, semicolons, quotations, and anything within parentheses (which typically just denotes an entity as a 
video game or a game developer). The names of people, which typically contain spaces, are joined together with an
underscore between them for use as the symbol for this entity in the reasoning system. 

#### Knowledge Generation
With the data properly cleaned and formatted, the dataframe can begin to be converted to Cyc-style knowledge 
triples for use in Companions. The code for generating the triples can be found within `TripleGenerator.py`. 

First, a set of triples are generated that specify the properties associated with each entity. This is done in the
function `create_triples_from_csv()`. For each row of the dataframe (i.e. each game), a new microtheory is created. This
is needed in order to perform analogical retrieval later. Then, for each column of the dataframe (i.e. each attribute),
the entities (e.g. a person) contained in this attribute cell for the current game, we create a new triple. 
For example, the director of *Rocket League* is Thomas Silloway. As a result, the 3-tuple of strings 
`('director', 'Rocket_League', 'Thomas_Silloway')` is generated. All of these triples are then stored in `triples.txt`,
 which is in the `data/` directory.  

After this, a second function, `generate_entity_instances()`, is called. This creates another file of triples that 
instantiates all of the entities that are referred to within the `triples.txt` file. This new file is called 
`instance_triples.txt` and is also stored in the `data/` directory. Each entity can be of part of an `isa` relation with 
one or more of VideoGame, VideoGameGenre, Person, Programmer, Artist, Writer, Composer, Director, Designer,
DevelopmentStudio, or System. 

Once the triples are created within the two text files, the function `generate_triples_krf()` is called to convert the
triples to the proper format and microtheory for use in Companions. These files are stored within the `knowledge/`
directory. At this point, the files are ready to be loaded into Companions and used for reasoning. 

In order to perform analogical retrieval based on each game represented in this system, it is necessary to group 
certain sets of facts into case libraries. This is done in the function `generate_case_library_krf()`. This function
will add each game's microtheory to the case library.

In total, we collected triples relating to 7433 games. In total, there were approximately 94000 triples in total, with
~62000 facts about ~32000 distinct entities.


#### Extending Companions Ontology
We build on top of the NextKB ontology provided within Companions. The complete set of entities, collections, predicates,
and relations that we defined for this project can be found in `knowledge/Video_Game_Ontology.krf`. The implementation
of the horn clauses for the predicates and relations can be found in `knowledge/Video_Game_Rules.krf`.

### Reasoning

We decided to use both analogical retrieval and case-based reasoning for our recommendations. Before we used Companions
built in analogical reasoning, we decided to do some pre-filtering on the games. We incorporated pre-existing domain 
knowledge, we determined that the recommended games should share at least one genre with one of the games the user 
provided for comparison.

We noted that for user friendliness, the entire reasoning process must happen without the user having to interact with
system more than for providing previously played games, and feedback on the results.

The reasoning process began with the user providing three games they had played in the past and enjoyed, with each
game having at least one corresponding aspect that the user really liked about the game (e.g. art, gameplay, story).
For each of these games, we dynamically created corresponding case libraries and added them as facts in Companions.
Only after we had inserted these libraries and all corresponding facts into Companions could the system proceed to
the analogical retrieval.

#### Analogical Retrieval

Perhaps the most unusual step in our recommendation system, at least based on video game recommendation systems out
there, was our analogical retrieval step. We hoped that the analogical reasoning - the finding the games with most
similar structures to the provided games, would prove fruitful in finding similar games in a novel manner. If a user
has liked games with many writers - games that tend to be either very large or episodic - then our system would generate
other games with many writers as candidates.

As a concrete example, querying Companions for similar games to Uncharted 4, a game with 3 listed designers, 1 artist,
1 composer, 3 programmers, and 2 directors, returns among others Telltale's Walking Dead, a game with an equal number
designers, programmers, directors, artists, and composers. Although the numbers aren't identical for all people who
worked on the game, Companions analogical reasoning does provide good candidates.  

Analogical reasoning is used in our system by taking the pre-filtered Case Libraries (each corresponding to one of
the games provided by the user), and queries Companions, e.g. `(reminding (KBCaseFn game1Mt) 
(CaseLibrarySansFn game1CaseLibrary game1Mt) (TheSet) ?mostsimilar ?matchinfo)`. We thus generate three different lists
of games corresponding to the three different games provided by the user.

#### Case-Based Reasoning

As recommendations often are (and should be) dependent on the preferences of the user, we decided that our system
should adjust its recommendations not only based on what the user liked about the games they initially provided,
but also on previous data about the user.

When the user provided 3 games to start the recommendation process, we also prompted them for information about which
aspects of the game they preferred. Each of these aspects mapped to one or more attributes in the games. If the user
said they liked the story, for example, that would map to the attribute `writer`. This serves two purposes. Firstly, it 
increases the impact matching writers have when finding the most viable candidates among those received from the 
analogical retrieval. Secondly, it increases (or decreases) the value of these attributes in subsequent recommendations, 
depending on the feedback the user provides about the recommendations.

To retain information about the user, the system stores a similarity vector, which is the final determinant in which
games the user is recommended. Initially each feature in the vector has equal weight 
(`writer=0.1, programmer=0.1,...,score=0.1`). Additionally, each recommended game carries its own game score vector.
The features in these vectors have positive values if they match one or more aspects of the (user provided) games that
generated these candidate games, else 0. 

After the user has been provided with a set of recommended video games, they are given the option to provide feedback.
The feedback the user provides after the recommendations determine the weights of the features for future 
recommendations. If the feedback is positive, the positive values are added to the similarity
vector. Else if it's negative, the values are subtracted from the feature vector. If the feedback is neutral, the
similarity vector remains unchanged. The vector is then normalized and stored to be used for future recommendations
for the same user. 