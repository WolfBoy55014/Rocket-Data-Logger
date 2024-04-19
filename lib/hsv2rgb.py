scalar = float  # a scale value (0.0 to 1.0)


def hsv2rgb(h: scalar, s: scalar, v: scalar) -> tuple:
    if s:
        if h == 1.0:
            h = 0.0
        i = int(h * 6.0)
        f = h * 6.0 - i

        w = int(255 * (v * (1.0 - s)))
        q = int(255 * (v * (1.0 - s * f)))
        t = int(255 * (v * (1.0 - s * (1.0 - f))))
        v = int(255 * v)

        if i == 0:
            return (v, t, w)
        if i == 1:
            return (q, v, w)
        if i == 2:
            return (w, v, t)
        if i == 3:
            return (w, q, v)
        if i == 4:
            return (t, w, v)
        if i == 5:
            return (v, w, q)
    else:
        v = int(255 * v)
        return (v, v, v)
