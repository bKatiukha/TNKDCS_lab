elements = {
    'pr1': {
        'name': 'Pr1',
        'failure_probability': 1.2 * 10e-4
    },
    'pr2': {
        'name': 'Pr2',
        'failure_probability': 1.2 * 10e-4
    },
    'pr3': {
        'name': 'Pr3',
        'failure_probability': 1.2 * 10e-4
    },
    'pr6': {
        'name': 'Pr6',
        'failure_probability': 1.2 * 10e-4
    },

    'a1': {
        'name': 'A1',
        'failure_probability': 1.1 * 10e-4
    },
    'a2': {
        'name': 'A2',
        'failure_probability': 1.1 * 10e-4
    },
    'a3': {
        'name': 'A3',
        'failure_probability': 1.1 * 10e-4
    },

    'c1': {
        'name': 'C1',
        'failure_probability': 1.9 * 10e-4
    },
    'c2': {
        'name': 'C2',
        'failure_probability': 1.9 * 10e-4
    },
    'c4': {
        'name': 'C4',
        'failure_probability': 1.9 * 10e-4
    },
    'c5': {
        'name': 'C5',
        'failure_probability': 1.9 * 10e-4
    },
    'c6': {
        'name': 'C6',
        'failure_probability': 1.9 * 10e-4
    },

    'd1': {
        'name': 'D1',
        'failure_probability': 3.2 * 10e-5
    },
    'd2': {
        'name': 'D2',
        'failure_probability': 3.2 * 10e-5
    },
    'd3': {
        'name': 'D3',
        'failure_probability': 3.2 * 10e-5
    },
    'd6': {
        'name': 'D6',
        'failure_probability': 3.2 * 10e-5
    },
    'd7': {
        'name': 'D7',
        'failure_probability': 3.2 * 10e-5
    },
    'd8': {
        'name': 'D8',
        'failure_probability': 3.2 * 10e-5
    },

    'b1': {
        'name': 'B1',
        'failure_probability': 1.4 * 10e-5
    },
    'b2': {
        'name': 'B2',
        'failure_probability': 1.4 * 10e-5
    },
    'b3': {
        'name': 'B3',
        'failure_probability': 1.4 * 10e-5
    },
    'b4': {
        'name': 'B4',
        'failure_probability': 1.4 * 10e-5
    },
    'b5': {
        'name': 'B5',
        'failure_probability': 1.4 * 10e-5
    },

    'm1': {
        'name': 'M1',
        'failure_probability': 3.3 * 10e-4
    },
    'c3': {
        'name': 'C3',
        'failure_probability': 1.9 * 10e-4
    },
    'd5': {
        'name': 'D5',
        'failure_probability': 3.2 * 10e-5
    },
    'm2': {
        'name': 'M2',
        'failure_probability': 3.3 * 10e-4
    },
}

elements_mod = {
    **elements,
    'c3': {
        'name': 'C3',
        'failure_probability': 1.9 * 10e-4
    },
    'm2': {
        'name': 'M2',
        'failure_probability': 3.3 * 10e-4
    },
}

load_table = {
    'pr1': {
        'nominal_load': 40,
        'max_load': 100,
        'redistributions': {
            'pr2': 30,
            'pr3': 40,
            'pr6': 10,
        }
    },
    'pr2': {
        'nominal_load': 70,
        'max_load': 100,
        'redistributions': {
            'pr1': 50,
            'pr3': 50,
            'pr6': 20,
        }
    },
    'pr3': {
        'nominal_load': 20,
        'max_load': 80,
        'redistributions': {
            'pr1': 20,
            'pr2': 20,
            'pr6': 20,
        }
    },
    'pr6': {
        'nominal_load': 50,
        'max_load': 80,
        'redistributions': {
            'pr1': 50,
            'pr2': 30,
            'pr3': 20,
        }
    }
}
