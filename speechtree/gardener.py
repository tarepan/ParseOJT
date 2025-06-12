"""Tree management tools."""

from itertools import chain

from speechtree.tree import AccentPhrase, Tree

# Check


def validate_tree(tree: Tree) -> None:
    """Place holder."""
    _ = tree


# Edit


def trim_head_tail_marks(tree: Tree) -> Tree:
    """Place holder."""
    if tree[0]["type"] == "MarkGroup":
        tree = tree[1:]
    if tree[-1]["type"] == "MarkGroup":
        tree = tree[:-1]
    return tree


def remove_group(tree: Tree, index: int) -> Tree:
    """Place holder."""
    _ = index
    return tree


# Output


def extract_text(tree: Tree) -> str:
    """Extract the text of the tree."""
    text = ""
    for gp in tree:
        for ap in gp["accent_phrases"]:
            for wd in ap["words"]:
                text += wd["text"]
    return text


def extract_pronunciation(tree: Tree) -> str:
    """Extract the pronunciation of the tree."""
    pronunciation = ""
    for gp in tree:
        for ap in gp["accent_phrases"]:
            for wd in ap["words"]:
                for mr in wd["moras"]:
                    pronunciation += mr["pronunciation"]
    return pronunciation


def extract_phonemes(
    tree: Tree, *, reduce_dup_pau: bool = True, distinguish_unvoicing: bool = True
) -> list[str]:
    """Place holder."""
    phonemes: list[str] = []
    for pg in tree:
        for ap in pg["accent_phrases"]:
            if reduce_dup_pau and pg["type"] == "MarkGroup":
                phonemes += ["pau"]
            else:
                for wd in ap["words"]:
                    for mora in wd["moras"]:
                        _ = distinguish_unvoicing
                        phonemes += [p["symbol"] for p in mora["phonemes"]]
    return phonemes


def extract_accent_position(ap: AccentPhrase) -> int:
    """Extract accent position of the accent phrase."""
    ap_moras = list(chain.from_iterable([wd["moras"] for wd in ap["words"]]))
    accent = len(ap_moras)
    for mora in reversed(ap_moras):
        if not mora["tone_high"]:
            accent -= 1
        else:
            break
    return accent
