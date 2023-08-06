import random
import fire
import emails

from collections import namedtuple
from typing import List, Tuple

MUTUAL_EXC = '_mutual_exc_'
EXCLUDED = '_excluded_'

__all__ = [
    'gen_pairs',
    'graph',
    'run',
    'run_and_email',
]

Response = namedtuple('Response', ['pairs', 'email'])


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


def graph(pairs: List[Tuple[str, str]], emoji=True) -> list:
    """
    Directed graph of generated pairs

    Args:
        pairs: list of two-element tuples
        emoji: show emoji or not

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
    while len(set(flatten(cp))) < len(pairs):
        cp.append(
            chain(pairs=[
                (k, v) for k, v in pairs
                if k not in flatten(cp)
            ])
        )
    sep = ' 🎁 >> ' if emoji else ' >> '
    return [sep.join(arrow) for arrow in cp]


def run(candidates: list, excluded: list = None, emoji=True):
    """
    Run generator directly

    Args:
        candidates: list of candidates
        excluded: list of excluded groups
        emoji: show emoji or not
    """
    pairs = gen_pairs(candidates=candidates, excluded=excluded)
    for c in graph(pairs=pairs, emoji=emoji):
        print(c)


def email_sender(sender_email: str, receiver_name: str, admin: dict):
    """
    Notify sender who's his/her receiver

    Args:
        sender_email: email address of the sender
        receiver_name: receiver's name
        admin: email settings of the administrator

    Returns:
        email response - status_code == 250 if sent successfully
    """
    subject = (
        admin.pop('subject', 'Your Destiny is ...')
        .replace('[receiver]', receiver_name)
    )

    body = (
        admin.pop('body', '')
        .replace('[receiver]', receiver_name)
    )
    if (receiver_name not in body) and (receiver_name not in subject):
        body += f'<br/>{receiver_name}'

    name = admin.pop('name', 'Your Host')
    email = admin.get('user')

    return (
        emails
        .html(
            html=body,
            subject=subject,
            mail_from=(name, email),
        )
        .send(
            to=sender_email,
            smtp=admin,
        )
    )


def run_and_email(
        admin: dict,
        address: dict,
        excluded: list = None,
        max_chains: int = 1,
) -> Response:
    """
    Run generator and email sender

    Args:
        admin: email settings of the administrator, including
               host - e.g., smtp.office365.com
               port - e.g., 587
               tls - True or False (must be False if ssl is True)
               ssl - True or False (must be False if tls is True)
               timeout - optional, default 10s
               user - email user name
               password - email password
               subject - opitonal, default something silly
               body - optional, default something silly as well
        address: participants name and email addresses
        excluded: mutually exclusive groups
        max_chains: max number of chains

    Returns:
        list of email responses
    """
    while True:
        pairs = gen_pairs(candidates=list(address.keys()), excluded=excluded)
        if len(graph(pairs=pairs)) <= max_chains:
            break

    return Response(
        pairs=pairs,
        email=[
            email_sender(
                sender_email=address[sender],
                receiver_name=receiver,
                admin=admin,
            )
            for sender, receiver in pairs
        ],
    )


def flatten(iterable):
    """
    Flatten any array of items to list

    Examples:
        >>> list(flatten(['ab', ['cd'], ['xy', 'zz']]))
        ['ab', 'cd', 'xy', 'zz']
        >>> list(flatten(['ab', ['xy', 'zz']]))
        ['ab', 'xy', 'zz']
    """
    from collections.abc import Iterable

    for elm in iterable:
        if isinstance(elm, Iterable) and not isinstance(elm, str):
            yield from flatten(elm)
        else: yield elm


if __name__ == '__main__':

    fire.Fire(run)
