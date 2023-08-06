from webcolors import name_to_rgb_percent


def normalize_color(color):
    if isinstance(color, tuple):
        if len(color) != 3 or min(v for v in color) < 0 or max(v for v in color) > 1:
            raise ValueError(
                "When specified as a tuple, color should be three floats between 0 and 1"
            )
        return color
    else:
        return tuple(0.01 * float(x.strip("%")) for x in name_to_rgb_percent(color))
