"""Functions such as Accuracy Calculation using the Stockfish Engine, for Aityz Chess."""

import stockfish
import matplotlib.pyplot as plt
import chess.pgn
import os
import re
import json
import requests
import random

USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0')

STOCKFISH_LOCATIONS = []

def clear_cache() -> None:
    """Clears all the cache for the Caching System.
    """
    cache_dir = 'aityz_cache'
    if os.path.exists(cache_dir):
        for file in os.listdir(cache_dir):
            os.remove(os.path.join(cache_dir, file))
        os.rmdir(cache_dir)

def sanitize_url(url: str) -> str:
    """Cleans URLs to be used in file names.

    Args:
        url (str): This URL will be used in the name of the file after being sanitized.

    Returns:
        str: A string with the cleansed URL.
    """
    url = url.replace('https://', '')
    url = re.sub(r'\W+', '-', url)
    return url

def save_subset(data: dict, url: str) -> None:
    """Save some JSON data to the Caching System.

    Args:
        data (dict): JSON formatted data that will be saved.
        url (str): The URL (that will be cleansed), and will eventually be the save location.
    """
    cache_dir = 'aityz_cache'
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
    safe_subset_name = sanitize_url(url)
    with open(os.path.join(cache_dir, f'{safe_subset_name}.json'), 'w') as f:
        json.dump(data, f, indent=4)

def load_subset(subset_name: str) -> dict:
    """Loads some JSON data from the Caching System.

    Args:
        subset_name (str): This will be an uncleansed URL that will be cleansed, and checked.

    Returns:
        dict: The JSON data for the subset.
    """
    safe_subset_name = sanitize_url(subset_name)
    with open(os.path.join('aityz_cache', f'{safe_subset_name}.json'), 'r') as f:
        data = json.load(f)
    return data

def find_subsets() -> list:
    """Lists all the cache that is stored in the Caching System.

    Returns:
        list: This will be a list of names (without the .json). They will be in Cleansed URL form.
    """
    cache_dir = 'aityz_cache'
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
        return []
    subsets = [file.replace('.json', '') for file in os.listdir(cache_dir)]
    return subsets

def get_pgns(username: str, verbose: bool = False) -> list:
    """Gets all the PGN formats of games from a user.

    Args:
        username (str): User to grab games from.
        verbose (bool, optional): Whether to print out the current subset. Defaults to False.

    Returns:
        list: A list of PGN formatted strings.
    """
    url = f'https://api.chess.com/pub/player/{username}/games/archives'
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    response.raise_for_status()
    subsets = response.json()
    cached = find_subsets()
    pgns = []
    for subset in subsets['archives']:
        sanitized_subset = sanitize_url(subset)
        if verbose:
            print(f'Fetching Subset {subset} ...!')
        if sanitized_subset in cached:
            data = load_subset(sanitized_subset)
        else:
            response = requests.get(subset, headers={'User-Agent': USER_AGENT})
            response.raise_for_status()
            data = response.json()
            save_subset(data, subset)
        for game in data['games']:
            try:
                pgns.append(game['pgn'])
            except:
                pass
    return pgns

def set_stockfish_location(location: str):
    """Set the location of the Stockfish executable to use.

    Args:
        location (str): A Path-like string that is where the Stockfish executable is located.
    """
    STOCKFISH_LOCATIONS.append(location)

def accuracy(pgn: str):
    """Calculates the accuracy as quickly as possible using the user's hardware.

    Args:
        pgn (str): A PGN formatted string of the game to analyse.

    Raises:
        Exception: If the stockfish location has not been set.

    Returns:
        float: A float between 0 and 100 representing the accuracy of the game.
    """
    if len(STOCKFISH_LOCATIONS) == 0:
        raise Exception("No stockfish locations set. Use set_stockfish_location(location) to set one.")
    engine = stockfish.Stockfish(STOCKFISH_LOCATIONS[0])
    with open("data.pgn", "w") as f:
        f.write(pgn)
    with open("data.pgn") as f:
        game = chess.pgn.read_game(f)
    
    best_moves = []
    moves = []
    board = game.board()

    for move in game.mainline_moves():
        try:
            moves.append(str(move))
            engine.set_fen_position(board.fen())
            best_moves.append(engine.get_best_move_time(5))
            board.push(move)
        except:
            engine = stockfish.Stockfish(STOCKFISH_LOCATIONS[0])
            board.push(move)
            best_moves.append(move)

    results = []

    for i in range(len(best_moves)):
        if best_moves[i] == moves[i]:
            results.append(1)
        else:
            results.append(0)
    try:
        result = sum(results) / len(results) * 100
    except:
        result = 50
    return result

def plot_accuracy(username: str, verbose: bool = False):
    """Plot the accuracy of a user over the span of their games.

    Args:
        username (str): The user to check.
        verbose (bool, optional): Whether to print the subsets. Defaults to False.
    """
    pgns = get_pgns(username, verbose=verbose)
    accuracies = []
    for pgn in pgns:
        print(f'Analysing game {pgns.index(pgn) + 1} of {len(pgns)}')
        accuracies.append(int(round(accuracy(pgn), 0)))
    
    plt.plot(accuracies)
    plt.title(f'Accuracy of {username}')
    plt.xlabel('Game')
    plt.ylabel('Accuracy (%)')
    plt.show()

def create_puzzle(username: str, verbose: bool = False):
    """Creates a puzzle from a random game of a user.

    Args:
        username (str): The user to check.
        verbose (bool, optional): Whether to print the subsets or not. Defaults to False.

    Returns:
        tuple: A tuple formatted with (GAME_FEN, UCI_FORMATTED_SOLUTION).
    """
    pgns = get_pgns(username, verbose=verbose)

    pgn = random.choice(pgns)

    with open('data.pgn', 'w') as f:
        f.write(pgn)
    with open('data.pgn', 'r') as f:
        game = chess.pgn.read_game(f)
    
    board = game.board()

    fens = []

    for move in game.mainline_moves():
        board.push(move)
        fens.append(board.fen())
    
    engine = stockfish.Stockfish(STOCKFISH_LOCATIONS[0])

    game = random.choice(fens)

    engine.set_fen_position(game)

    puzzle = engine.get_best_move_time(1000)

    return (game, puzzle)

def create_puzzles(username: str, count: int, verbose: bool = False, interval: int = 1000):
    """Creates multiple puzzles from a user.

    Args:
        username (str): The user to check.
        count (int): The amount of puzzles to create.
        verbose (bool, optional): Whether to print the subsets or not. Defaults to False.
        interval (int, optional): How many seconds to give the engine to calculate the best move. Defaults to 1000.

    Returns:
        list: A list of tuples formatted with (GAME_FEN, UCI_FORMATTED_SOLUTION).
    """
    puzzles = []
    
    pgns = get_pgns(username, verbose=verbose)

    pgn = random.choice(pgns)

    with open('data.pgn', 'w') as f:
        f.write(pgn)
    with open('data.pgn', 'r') as f:
        game = chess.pgn.read_game(f)
    
    board = game.board()

    fens = []

    for move in game.mainline_moves():
        board.push(move)
        fens.append(board.fen())
    
    engine = stockfish.Stockfish(STOCKFISH_LOCATIONS[0])

    for i in range(count):
        game = random.choice(fens)

        engine.set_fen_position(game)

        puzzle = engine.get_best_move_time(interval)

        puzzles.append((game, puzzle))

    return puzzles

def elo_calculation(pgn: str, upper_bounds: int = 3000, ms_per_move=50, progress_bar=True):
    """Calculates the Elo rating of a game. Takes about 1.5 seconds per move, by default. Adjusting the Upper Bounds parameter reduces time.

    Args:
        pgn (str): The PGN of the chess game.
        upper_bounds (int, optional): Maximum to check for. Defaults to 3000.
        ms_per_move (int, optional): How many milliseconds to give the engine to calculate the best move. Defaults to 50.
        progress_bar (bool, optional): Whether to show a progress bar or not. Defaults to True.
    
    Returns:
        int: The Elo rating of the game.
    """

    with open("data.pgn", "w") as f:
        f.write(pgn)
    with open("data.pgn", 'r') as f:
        game = chess.pgn.read_game(f)
    
    board = game.board()

    checking = []

    for i in range(int((upper_bounds / 50) - 10)):
        checking.append((i+10) * 50)

    elos = []

    engine = stockfish.Stockfish(STOCKFISH_LOCATIONS[0])
    for movee in game.mainline_moves():
        temp_elos = []
        for i in checking:
            engine.set_fen_position(board.fen())
            engine.set_elo_rating(i)
            move = engine.get_best_move_time(ms_per_move)
            if move == str(movee):
                temp_elos.append(i)
                break
        try:
            if max(temp_elos) != 0:
                elos.append(max(temp_elos))
        except:
            pass
        
        board.push(movee)

    return sum(elos) / len(elos)  
