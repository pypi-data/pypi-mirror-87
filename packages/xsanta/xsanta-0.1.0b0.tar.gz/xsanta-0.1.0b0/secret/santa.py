import random
import fire

from typing import List, Tuple
from xone import utils

from secret import __version__

MUTUAL_EXC = '_mutual_exc_'
EXCLUDED = '_excluded_'

__all__ = [
    '__version__',
    'gen_pairs',
    'graph',
    'run',
]


def verify_pair(sender: str, receiver: str) -> bool:
    """
    Verify if pair is valid

    1) Sender should not gift him/herself
    2) Receiver should not gift his/her sender
    3) People from same family or of certain familiarities
       should not gift each other

    Args:
        sender: sender name
        receiver: receiver name

    Returns:
        Boolean of validity of pair
    """
    # Rule #1
    if sender == receiver:
        return False

    # Rule #2
    if {sender, receiver} in globals().get(MUTUAL_EXC, []):
        return False

    # Rule #3
    for cp in globals().get(EXCLUDED, []):
        if not {sender, receiver}.difference(set(cp)):
            return False

    # Add pair of sender / receiver to existing list
    if MUTUAL_EXC not in globals():
        globals()[MUTUAL_EXC] = []
    globals()[MUTUAL_EXC].append({sender, receiver})
    return True


def gen_pairs(candidates: list, excluded: list = None) -> list:
    """
    Generate pairs of sender / receiver

    Args:
        candidates: list of candidates
        excluded: list of excluded groups of sender / receiver

    Returns:
        list of matched pairs
    """
    alice = candidates[:]
    bob = candidates[:]
    globals()[EXCLUDED] = [] if excluded is None else excluded
    while True:
        random.shuffle(bob)
        globals()[MUTUAL_EXC] = []
        if all(map(verify_pair, alice, bob)):
            return list(zip(alice, bob))


def chain(pairs: List[Tuple[str, str]]) -> list:
    """
    Single directed graph from given dict

    Args:
        pairs: list of pairs of sender / receiver

    Returns:
        list of gift chains

    Examples:
        >>> c = chain([
        ...     ('Alice', 'Eve'),
        ...     ('Bob', 'Alice'),
        ...     ('Eve', 'Bob'),
        ... ])
        >>> c in [
        ...     ['Alice', 'Eve', 'Bob', 'Alice'],
        ...     ['Eve', 'Bob', 'Alice', 'Eve'],
        ...     ['Bob', 'Alice', 'Eve', 'Bob'],
        ... ]
        True
    """
    init = random.choice(pairs)[0]
    sender, res = init, [init]
    p_dict = dict(pairs)
    while True:
        receiver = p_dict[sender]
        res.append(receiver)
        sender = receiver
        if receiver == init: break
    return res


def graph(pairs: List[Tuple[str, str]]) -> list:
    """
    Directed graph of generated pairs

    Args:
        pairs: list of two-element tuples

    Returns:
        list of string

    Examples:
        >>> g = graph([
        ...     ('Alice', 'Bob'),
        ...     ('Bob', 'Eve'),
        ...     ('Eve', 'Alice'),
        ... ])[0]
        >>> g in [
        ...     'Alice 🎁 >> Bob 🎁 >> Eve 🎁 >> Alice',
        ...     'Bob 🎁 >> Eve 🎁 >> Alice 🎁 >> Bob',
        ...     'Eve 🎁 >> Alice 🎁 >> Bob 🎁 >> Eve',
        ... ]
        True
    """
    cp = []
    while len(utils.flatten(cp, unique=True)) < len(pairs):
        cp.append(
            chain(pairs=[
                (k, v) for k, v in pairs
                if k not in utils.flatten(cp)
            ])
        )
    return [' 🎁 >> '.join(arrow) for arrow in cp]


def run(candidates: list, excluded: list = None):
    """
    Run generator directly

    Args:
        candidates: list of candidates
        excluded: list of excluded groups
    """
    for c in graph(gen_pairs(candidates=candidates, excluded=excluded)):
        print(c)


if __name__ == '__main__':

    fire.Fire(run)
