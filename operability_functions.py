def f1(modules):
    return (
        (
            (modules["d1"] or modules["d2"])
            and modules["c1"]
            or
            (modules["d2"] or modules["d3"])
            and modules["c2"]
        )
        and (modules["b1"] or modules["b2"])
        and (modules["pr1"] or modules["pr2"])
    )


def f2(modules):
    return (
        modules["d6"]
        and modules["c4"]
        and modules["m1"]
        and (
            (
                modules["a1"]
                and (modules["b1"] or modules["b2"])
                and modules["pr3"]
            ) or (
                modules["a2"]
                and (modules["b3"] or modules["b5"])
                and modules["pr6"]
            )
        )
    )


def f3(modules):
    return (
        (modules["d7"] or modules["d8"])
        and modules["c5"]
        and modules["b3"]
        and modules["pr6"]
    )


def f4(modules):
    return (
        modules["d8"]
        and modules["c6"]
        and (
            ((modules["b4"] or modules["b3"]) and modules["pr6"])
            or (
                modules["b3"]
                and modules["a3"]
                and modules["b5"]
                and modules["a2"]
                and modules["m1"]
                and modules["a1"]
                and (modules["b1"] or modules["b2"])
                and modules["pr2"] or modules["pr3"]
            )
        )
    )


def logical_structure_function(modules):
    return (
        f1(modules)
        and f2(modules)
        and f3(modules)
        and f4(modules)
    )


def f2_mod(modules):
    return (
        (modules["d6"])
        and (modules["c4"])
        and (modules["m1"] or modules["m2"])
        and (
            (
                modules["a1"]
                and (modules["b1"] or modules["b2"])
                and modules["pr3"]
            ) or (
                modules["a2"]
                and (modules["b3"] or modules["b5"])
                and modules["pr6"]
            )
        )
    )


def f3_mod(modules):
    return (
        (modules["d7"] or modules["d8"])
        and ((modules["c6"] and (modules["b3"] or modules["b4"]) and modules["pr6"]) or (
                (modules["c5"] or modules["c6"])
                and modules["b3"]
                and modules["pr6"]
            )
        )
    )


def f4_mod(modules):
    return (
        (modules["d7"] or modules["d8"])
        and (
            (
                (modules["c6"]) and (modules["b4"] or modules["b3"])
                or (modules["c5"] and modules["b3"])
            ) and modules["pr6"]
            or (
                modules["c6"]
                and modules["b3"]
                and modules["a3"]
                and modules["b5"]
                and modules["a2"]
                and (modules["m1"] or modules["m2"])
                and modules["a1"]
                and (modules["pr2"] or modules["pr3"])
            )
        )
    )


def logical_structure_function_mod(modules):
    return (
        f1(modules)
        and f2_mod(modules)
        and f3_mod(modules)
        and f4_mod(modules)
    )


def f2_mod2(modules):
    return (
        (modules["d6"] or modules["d5"])
        and (modules["c4"] or modules["c3"])
        and (modules["m1"] or modules["m2"])
        and (
            (
                modules["a1"]
                and (modules["b1"] or modules["b2"])
                and modules["pr3"]
            ) or (
                modules["a2"]
                and (modules["b3"] or modules["b5"])
                and modules["pr6"]
            )
        )
    )


def logical_structure_function_mod2(modules):
    return (
        f1(modules)
        and f2_mod2(modules)
        and f3_mod(modules)
        and f4_mod(modules)
    )