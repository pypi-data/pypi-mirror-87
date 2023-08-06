# LibreFi
## Free Wi-Fi was so great that we created Free Wi-Fi 2

Note: work is still in progress, this is not stable, may not be usable or useful

## How to use:
release (not to be confused with: _stable_):
```sh
# you may want to use python3.9, python2, python, jython or something like that
$ python3 -m pip install librefi
$ python3 -m librefi	# no daemon yet, run to connect
```

development:
```sh
$ git clone https://git.sakamoto.pl/laudom/librefi.git
$ cd librefi
$ pip3 install -r ./requirements.txt
$ pip3 install -r ./requirements_dev.txt
$ python3 -m librefi	# no daemon yet, run to connect
```

## A bit of technical things
- Requires Python 3.4+ or 2.7 (preferably 3.8+)
- Requires NetworkManager (only Linux and some Unix-like systems) to connect with Wi-Fi networks for now, however, it's ready to implement other connectors.
- Only tested with CPython and Jython, other implementations may work by accident.
- Only works with [these networks](https://git.sakamoto.pl/laudom/librefi/-/blob/master/librefi/fxckers/_map.py)

## Contributing
If you want to contribute, please contact with either [Lauren](https://selfisekai.rocks) or [Dominika](https://sakamoto.pl) for a [git.sakamoto.pl](https://git.sakamoto.pl) account, or just [submit patches by e-mail](https://devconnected.com/how-to-create-and-apply-git-patch-files/#Create_Git_Patch_Files) to <librefi-patches@selfisekai.rocks>

## Maintainers:
### Core:
- Lauren Liberda <lauren@selfisekai.rocks>
- Dominika Liberda <sdomi@sakamoto.pl>
### Fxckers:
- Poland:
    - Warsaw:
        - Lauren Liberda <lauren@selfisekai.rocks>
        - Dominika Liberda <sdomi@sakamoto.pl>
