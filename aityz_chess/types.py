"""This module contains the types for Aityz Chess."""

from typing import Any, List
import requests

USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0')

class PGNGenerator:
    def __init__(self, games: list):
        """A PGN generator that can be used with other sub-modules in Aityz Chess.

        Args:
            games (list): A list of PGNS in String Format.
        
        Attributes:
            games (list): A list of PGNS in String Format.
        """
    
        self.games = games

    def __iter__(self):
        """This is an iterator for the PGNGenerator class.

        Yields:
            str: The next PGN in the list of games.
        """
        for game in self.games:
            yield game
        
    def __len__(self):
        """This is a length function for the PGNGenerator class.

        Returns:
            int: The length of the list of games.
        """
        return len(self.games)

class Stats:
    def __init__(self, data: dict):
        """A Stats object that can be used with other sub-modules in Aityz Chess.

        Args:
            data (dict): The data for the stats.

        Attributes:
            data (dict): All of the data available for the stats.
            chess_blitz (int): The chess blitz rating of the user.
            chess_bullet (int): The chess bullet rating of the user.
            chess_daily (int): The chess daily rating of the user.
            chess_rapid (int): The chess rapid rating of the user.
            tactics (int): The tactics rating of the user.
            lessons (int): The lessons rating of the user.
            puzzle_rush (int): The puzzle rush rating of the user.
        """

        self.data = data

        modes = ['chess_blitz', 'chess_bullet', 'chess_daily', 'chess_rapid', ]

        for mode in modes:
            try:
                setattr(self, mode, data[mode]['last']['rating'])
            except:
                setattr(self, mode, None)
        
        modes = ['tactics', 'lessons', 'puzzle_rush']

        for mode in modes:
            try:
                setattr(self, mode, data[mode]['best']['rating'])
            except:
                setattr(self, mode, None)
    
    def __str__(self) -> str:
        """This is a string function for the Stats class.

        Returns:
            str: A string representation of the Stats object.
        """
        return "<Stats: {}>".format(self.chess_rapid)
    
    def __repr__(self) -> str:
        """This is a representation function for the Stats class.

        Returns:
            str: A string representation of the Stats object.
        """
        return "<Stats: {}>".format(self.chess_rapid)

class Profile:
    def __init__(self, data: dict):
        """A Profile object that can be used with other sub-modules in Aityz Chess.

        Args:
            data (dict): The data for the profile.
        
        Attributes:
            data (dict): All of the data available for the profile.
            id (str): The ID of the profile.
            url (str): The URL of the profile.
            username (str): The username of the profile.
            player_id (int): The player ID of the profile.
            status (str): The status of the profile.
            title (str): The title of the profile.
            name (str): The name of the profile.
            avatar (str): The avatar of the profile.
            location (str): The location of the profile.
            country (str): The country of the profile.
            joined (int): The time the user joined the profile.
            last_online (int): The time the user was last online.
            followers (int): The number of followers the user has.
            is_streamer (bool): Whether the user is a streamer or not.
            twitch_url (str): The Twitch URL of the user.
            fide (int): The FIDE rating of the user.
        """
        self.data = data
        self.id = data['@id']
        self.url = data['url']
        self.username = data['username']
        self.player_id = data['player_id']
        self.status = data['status']

        fields = ['title', 'name', 'avatar', 'location', 'country', 'joined', 'last_online', 'followers', 'is_streamer', 'twitch_url', 'fide']

        for field in fields:
            try:
                setattr(self, field, data[field])
            except:
                setattr(self, field, None)
    
    def __str__(self) -> str:
        """This is a string function for the Profile class.

        Returns:
            str: A string representation of the Profile object.
        """
        return "<Profile: {}>".format(self.username)
    
    def __repr__(self) -> str:
        """This is a representation function for the Profile class.

        Returns:
            str: A string representation of the Profile object.
        """
        return "<Profile: {}>".format(self.username)
    
    def fulfill_stats(self) -> Stats:
        """Fulfills the Profile object with stats.

        Returns:
            Stats: A Stats object.
        """
        url = f'https://api.chess.com/pub/player/{self.username}/stats'
        response = requests.get(url, headers={'User-Agent': USER_AGENT})
        response.raise_for_status()
        data = response.json()
        return Stats(data)

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

class TitledPlayer:
    def __init__(self, name):
        """A TitledPlayer object that can be used with other sub-modules in Aityz Chess.

        Args:
            name (str): The name of the titled player.

        Attributes:
            name (str): The name of the titled player.
        """
        self.name = name
    
    def fulfill(self) -> Profile:
        """Fulfills the TitledPlayer object.

        Returns:
            Profile: A Profile object.
        """
        return get_profile(self.name)
    
    def __str__(self) -> str:
        """This is a string function for the TitledPlayer class.

        Returns:
            str: A string representation of the TitledPlayer object.
        """
        return "<TitledPlayer: {}>".format(self.name)
    
    def __repr__(self) -> str:
        """This is a representation function for the TitledPlayer class.

        Returns:
            str: A string representation of the TitledPlayer object.
        """
        return "<TitledPlayer: {}>".format(self.name)

class DailyGame:
    def __init__(self, data: dict):
        """A DailyGame object that can be used with other sub-modules in Aityz Chess. All of the attributes are optional.

        Args:
            data (dict): The data for the daily game.

        Attributes:
            data (dict): All of the data available for the daily game.
            url (str): The URL of the daily game.
            pgn (str): The PGN of the daily game.
            time_class (str): The time class of the daily game.
            time_control (int): The time control of the daily game.
            rules (str): The rules of the daily game.
            fen (str): The FEN of the daily game.
            rated (bool): Whether the daily game is rated or not.
            clock (dict): The clock of the daily game.
            white (dict): The white player of the daily game.
            black (dict): The black player of the daily game.
            tournament (dict): The tournament of the daily game.
            match (dict): The match of the daily game.
        """

        modes = ['white', 'black', 'url', 'fen', 'pgn', 'time_class', 'time_control', 'rules', 'rated', 'clock', 'time_class', 'time_control', 'time_class', 'rules', 'tournament', 'match']

        for mode in modes:
            try:
                setattr(self, mode, data[mode])
            except:
                setattr(self, mode, None)

class DailyGameGenerator:
    def __init__(self, games: list):
        """A DailyGameGenerator object that can be used with other sub-modules in Aityz Chess.

        Args:
            games (list): A list of DailyGame objects.
        
        Attributes:
            games (list): A list of DailyGame objects.
        """
        self.games = games
    
    def __iter__(self):
        """This is an iterator for the DailyGameGenerator class.

        Yields:
            DailyGame: The next DailyGame in the list of games.
        """
        for game in self.games:
            yield game
    
    def __len__(self):
        """This is a length function for the DailyGameGenerator class.

        Returns:
            int: The length of the list of games.
        """
        return len(self.games)

class Club:
    def __init__(self, data: dict):
        """A Club object that can be used with other sub-modules in Aityz Chess. All the attributes may not be fulfilled, such as icon, if the icon has not been set.

        Args:
            data (dict): The data for the club.

        Attributes:
            data (dict): All of the data available for the club.
            ``@id`` (str): The ID of the club.
            name (str): The name of the club.
            last_activity (int): The last activity of the club.
            icon (str): The icon of the club.
            url (str): The URL of the club.
            joined (int): The time the user joined the club.
        """

        self.data = data

        fields = ['@id', 'name', 'last_activity', 'icon', 'url', 'joined']

        for field in fields:
            try:
                setattr(self, field, data[field])
            except:
                setattr(self, field, None)
    
    def __str__(self) -> str:
        """This is a string function for the Club class.

        Returns:
            str: A string representation of the Club object.
        """
        return "<Club: {}>".format(self.name)
    
    def __repr__(self) -> str:
        """This is a representation function for the Club class.

        Returns:
            str: A string representation of the Club object.
        """
        return "<Club: {}>".format(self.name)

class Tournament:
    def __init__(self, data: dict):
        """Represents a Tournament on Chess.com. All attributes are optional, and maybe not be fulfilled by chess.com.

        Args:
            data (dict): The data for the tournament.

        Attributes:
            url (str): The URL of the tournament.
            ``@id`` (str): The ID of the tournament.
            wins (int): The number of wins the user has in the tournament.
            losses (int): The number of losses the user has in the tournament.
            draws (int): The number of draws the user has in the tournament.
            points_awarded (int): The number of points the user has been awarded in the tournament.
            placement (int): The placement of the user in the tournament.
            status (str): The status of the tournament.
            total_players (int): The total number of players in the tournament.
        """
        fields = ['url', '@id', 'wins', 'losses', 'draws', 'points_awarded', 'placement', 'status', 'total_players']

        for field in fields:
            try:
                setattr(self, field, data[field])
            except:
                setattr(self, field, None)
    
    def __str__(self) -> str:
        """This is a string function for the Tournament class.

        Returns:
            str: A string representation of the Tournament object.
        """
        return "<Tournament: {}>".format(self.url)
    
    def __repr__(self) -> str:
        """This is a representation function for the Tournament class.

        Returns:
            str: A string representation of the Tournament object.
        """
        return "<Tournament: {}>".format(self.url)

class TournamentGenerator:
    def __init__(self, tournaments: list):
        """A TournamentGenerator object that can be used with other sub-modules in Aityz Chess.

        Args:
            tournaments (list): A list of Tournament objects.

        Attributes:
            tournaments (list): A list of Tournament objects.
        """
        self.tournaments = tournaments
    
    def __iter__(self):
        """This is an iterator for the TournamentGenerator class.

        Yields:
            Tournament: The next Tournament in the list of tournaments.
        """
        for tournament in self.tournaments:
            yield tournament
    
    def __len__(self):
        """This is a length function for the TournamentGenerator class.

        Returns:
            int: The length of the list of tournaments.
        """
        return len(self.tournaments)
    
class PartialProfile:  # TODO TitledPlayer to extend PartialProfile
    def __init__(self, data: dict):
        """A PartialProfile object that can be used with other sub-modules in Aityz Chess.

        Args:
            data (dict): The data for the partial profile.

        Attributes:
            username (str): The username of the partial profile.
            data (dict): All of the data available for the partial profile.
        """
        self.data = data
        self.username = data['username']

    def __str__(self) -> str:
        """This is a string function for the PartialProfile class.

        Returns:
            str: A string representation of the PartialProfile object.
        """
        return "<PartialProfile: {}>".format(self.username)
    
    def __repr__(self) -> str:
        """This is a representation function for the PartialProfile class.

        Returns:
            str: A string representation of the PartialProfile object.
        """
        return "<PartialProfile: {}>".format(self.username)
    

class Leaderboard:
    def __init__(self, data: dict):
        """A Leaderboard object that can be used with other sub-modules in Aityz Chess.

        Args:
            data (dict): The data for the leaderboard.

        Attributes:
            daily (dict): The daily leaderboard.
            daily_960 (dict): The daily 960 leaderboard.
            rapid (dict): The rapid leaderboard.
            blitz (dict): The blitz leaderboard.
            bullet (dict): The bullet leaderboard.
            bughouse (dict): The bughouse leaderboard.
            blitz_960 (dict): The blitz 960 leaderboard.
            threecheck (dict): The threecheck leaderboard.
            crazyhouse (dict): The crazyhouse leaderboard.
            kingofthehill (dict): The king of the hill leaderboard.
            tactics (dict): The tactics leaderboard.
        """
        self.daily = data['daily']
        self.daily_960 = data['daily960']
        self.rapid = data['live_rapid']
        self.blitz = data['live_blitz']
        self.bullet = data['live_bullet']
        self.bughouse = data['live_bughouse']
        self.blitz_960 = data['live_blitz960']
        self.threecheck = data['live_threecheck']
        self.crazyhouse = data['live_crazyhouse']
        self.kingofthehill = data['live_kingofthehill']
        self.tactics = data['tactics']

    def __str__(self):
        """This is a string function for the Leaderboard class.
        
        Returns:
            str: A string representation of the Leaderboard object.
        """
        return "<Leaderboard>"
    
    def __repr__(self):
        """This is a representation function for the Leaderboard class.
        
        Returns:
            str: A string representation of the Leaderboard object.
        """
        return "<Leaderboard>"

