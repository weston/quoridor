# quoridor.py

quoridor.py is a python package that allows you to write bots that play quoridor against eachother, or against humans.

## Getting Started

I have included some very dumb quoridor bots that are able to play versus eachother. To create a new quoridor bot, you have to subclass the `QuoridorBasePlayer` in `quoridor_base_player.py`.  Examples of this can be found in `random_player.py`, `no_fence_player.py`, and `bfs_player.py`.


## Playing games
You can start a game by running 

```python quoridor_game.py```


```
Welcome to Quoridor

Please specify the player classes you want to use

Leave blank for human_player:HumanPlayer

class for player 0:
```

To pit BFSPlayer vs NoFencePlayer, we can enter:

```bfs_player:BFSPlayer```

```enter some name```

```no_fence_player:NoFencePlayer```

```enter some other name```

They will then proceed to play the game of quoridor and the outcome will be printed to the stdout.

You can also choose to view the gameplay history dump at the end of the game.

How exciting!
