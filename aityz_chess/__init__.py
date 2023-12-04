"""Aityz Chess is a Python library that allows you to interact with the Chess.com API, and perform analysis."""

import requests
from .types import *
from .cache import *

USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0')

def get_user_pgns(username: str, verbose: bool = False):
    """Gets all the PGNs of a user, using the caching system.
    
    Args:
        username (str): The username of the user.
        verbose (bool, optional): Whether to print the progress of the fetching. Defaults to False.
        
    Returns:
        PGNGenerator: A PGNGenerator object that can be used to iterate over the PGNs."""
    
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
    return PGNGenerator(pgns)

def get_profile(username: str) -> Profile:
    """Gets a Profile object for a given username.
    
    Args:
        username (str): The username of the user.
        
    Returns:
        Profile: A Profile object that can be used with other sub-modules in Aityz Chess."""
    
    url = f'https://api.chess.com/pub/player/{username}'
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    response.raise_for_status()
    data = response.json()
    return Profile(data)

def get_titled(title: str) -> List[TitledPlayer]:
    """Get a list of titled players.

    Returns:
        List[Profile]: A list of Profile objects.
    """
    url = f'https://api.chess.com/pub/titled/{title}'
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    response.raise_for_status()
    data = response.json()
    profiles = []
    for profile in data['players']:
        profiles.append(TitledPlayer(profile))
    return profiles

def get_daily_games(username: str) -> DailyGameGenerator:
    """Gets all the daily games of a user.

    Args:
        username (str): The username of the user.

    Returns:
        DailyGameGenerator: A DailyGameGenerator object that can be used to iterate over the daily games.
    """
    data = requests.get(f'https://pub/player/{username}/games', headers={'User-Agent': USER_AGENT}).json()

    games_list = []

    for game in data['games']:
        games_list.append(DailyGame(game))
    
    return DailyGameGenerator(games_list)

def get_daily_games_to_move(usename: str) -> DailyGameGenerator:
    """Gets all the daily games of a user where it is the user's turn to move.

    Args:
        usename (str): The use to check for.

    Returns:
        DailyGameGenerator: A DailyGameGenerator object that can be used to iterate over the daily games.
    """
    data = requests.get(f'https://pub/player/{usename}/games/to-move', headers={'User-Agent': USER_AGENT}).json()

    games_list = []

    for game in data['games']:
        games_list.append(DailyGame(game))
    
    return DailyGameGenerator(games_list)

def get_tournaments(username: str) -> TournamentGenerator:
    """Gets all the tournaments of a user.

    Args:
        username (str): The username of the user.

    Returns:
        TournamentGenerator: A TournamentGenerator object that can be used to iterate over the tournaments.
    """
    data = requests.get(f'https://pub/player/{username}/tournaments', headers={'User-Agent': USER_AGENT}).json()

    tournaments_list = []

    for tournament in data['finished']:
        tournaments_list.append(Tournament(tournament))
    
    return TournamentGenerator(tournaments_list)

def get_club_by_id(id: str) -> Club:
    """Get a Club object by the ID.
    
    Args:
        id (str): The ID of the tournament to check.
    
    Returns:
        Club: A Club object from Aityz Chess."""
    
    url = f'https://api.chess.com/pub/club/{id}'
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    response.raise_for_status()
    data = response.json()
    return Club(data)

def get_club_members(club: Club) -> List[PartialProfile]:
    """Get a list of members in a club.
    
    Args:
        club (Club): The club to check.
    
    Returns:
        List[Profile]: A list of Profile objects."""
    
    url = f'https://api.chess.com/pub/club/{club.id}/members'
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    response.raise_for_status()
    data = response.json()
    profiles = []
    for profile in data['all_time']:
        profiles.append(PartialProfile(profile))
    return profiles

def get_tournament_by_id(id: str) -> Tournament:
    """Get a Tournament object by the ID.
    
    Args:
        id (str): The ID of the tournament to check.
    
    Returns:
        Tournament: A Tournament object from Aityz Chess."""
    
    url = f'https://api.chess.com/pub/tournament/{id}'
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    response.raise_for_status()
    data = response.json()
    return Tournament(data)

def get_leaderboard() -> Leaderboard:
    """Get the current leaderboard.
    
    Returns:
        Leaderboard: A Leaderboard object from Aityz Chess."""
    
    url = f'https://api.chess.com/pub/leaderboards'
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    response.raise_for_status()
    data = response.json()
    return Leaderboard(data)
