# -*- coding: utf-8 -*-

import bitarray
import auxillary
import math
import random


class ReliabilityCalculator(object):
    def __init__(self, elements, logical_structure_function, load_table):
        self._elements = elements
        self._logical_structure_function = logical_structure_function
        self._load_table = load_table
        self._statistics = None
        self._reliabilities = []

    def calculate_simple_reliability(self):
        result = 0.0
        keys = list(self._elements.keys())
        count_of_elements = len(self._elements)
        for i in range(0, 2 ** count_of_elements):
            states_vector = bitarray.bitarray(auxillary.to_binary(i)[64 - count_of_elements:])
            table_of_states = {keys[j]: states_vector[j] for j in range(count_of_elements)}
            probability_of_state = auxillary.calculate_probability_of_system_state(table_of_states, self._elements)
            will_system_work = self._logical_structure_function(table_of_states)
            if will_system_work:
                result += probability_of_state

        return result

    def calculate_reliability_without_failures(self):
        """
        Вероятность того, что в системе не будет отказов.
        :return:
        """
        result = 0.0
        keys = list(self._elements.keys())
        count_of_elements = len(self._elements)

        states_vector = bitarray.bitarray(count_of_elements)
        states_vector.setall(True)
        table_of_states = {keys[j]: states_vector[j] for j in range(count_of_elements)}
        probability_of_state = auxillary.calculate_probability_of_system_state(table_of_states, self._elements)
        will_system_work = self._logical_structure_function(table_of_states)
        if will_system_work:
            result += probability_of_state

        return result

    def calculate_reliability_with_n_failures(self, count_of_failures, percent_of_possible_vectors_to_generate, use_active_failover):
        """
        Вероятность того, что в системе случится ровно count_of_failures отказов, но она останется работоспособной.
        :param count_of_failures:
        :param percent_of_possible_vectors_to_generate:
        :return:
        """
        result = 0.0
        keys = list(self._elements.keys())
        count_of_elements = len(self._elements)

        count_of_vectors = math.factorial(count_of_elements) // (math.factorial(count_of_failures) * math.factorial(count_of_elements - count_of_failures))
        count_of_vectors = int(count_of_vectors * percent_of_possible_vectors_to_generate)
        states_vector = bitarray.bitarray(count_of_elements)
        states_vector.setall(True)
        bad_states = set()
        for vector_number in range(count_of_vectors):
            zero_positions = self._add_new_bad_state(bad_states, count_of_failures, count_of_elements)
            auxillary.invert_at_positions(states_vector, zero_positions)

            table_of_states = {keys[j]: states_vector[j] for j in range(count_of_elements)}
            probability_of_state = auxillary.calculate_probability_of_system_state(table_of_states, self._elements)
            will_system_work = self._logical_structure_function(table_of_states) or \
                               (self.can_load_be_redistributed(table_of_states) and use_active_failover)
            if will_system_work:
                result += probability_of_state
            else:
                for key in table_of_states.keys():
                    if not table_of_states[key]:
                        self._statistics[key] += 1

                        # # Create a copy of the table of states to avoid modifying the original
                        # table_of_states_copy = table_of_states.copy()
                        #
                        # # Set the current state to 1 in the copied dictionary
                        # table_of_states_copy[key] = 1
                        #
                        # # Check if the system can work again
                        # will_system_work_again = (
                        #         self._logical_structure_function(table_of_states_copy) or
                        #         (self.can_load_be_redistributed(table_of_states_copy) and use_active_failover)
                        # )
                        #
                        # # If the system can work again, increment the statistics
                        # if will_system_work_again:
                        #     self._statistics[key] += 1

            auxillary.invert_at_positions(states_vector, zero_positions)
        return result / percent_of_possible_vectors_to_generate

    def calculate_reliability(self, use_active_failover=False):
        self._statistics = {
            key: 0 for key in self._elements
            }

        self._reliabilities = [
            self.calculate_reliability_without_failures(),
            self.calculate_reliability_with_n_failures(1, 1.0, use_active_failover),
            self.calculate_reliability_with_n_failures(2, 1.0, use_active_failover),
            self.calculate_reliability_with_n_failures(3, 0.5, use_active_failover),
            self.calculate_reliability_with_n_failures(4, 0.1, use_active_failover)
        ]

        return sum(self._reliabilities)

    def can_load_be_redistributed(self, table_of_states):
        # Вибір модулів, що відмовили і які присутні в обох таблицях - у поточному стані та в таблиці навантаження
        interesting_modules = {key for key in table_of_states.keys() if
                               key in self._load_table.keys() and not table_of_states[key]}

        # Якщо немає жодного модуля, що відмовив, перерозподіл не потрібен, повертаємо False
        if len(interesting_modules) == 0:
            return False

        # Створюємо таблицю перерозподілу навантаження для кожного з модуля
        # Визначаємо для кожного відмовленого модуля, на які інші модулі можна перенести його навантаження
        table_of_redistribution = {
            key: frozenset(
                redistribution_target for redistribution_target in self._load_table[key]['redistributions']
                if redistribution_target not in interesting_modules
            ) for key in interesting_modules
        }

        # Перевірка: чи всі відмовлені модулі мають хоча б одну можливість для перерозподілу
        if len(table_of_redistribution) != len(interesting_modules):
            return False

        # Перевірка: чи достатньо навантаження можна компенсувати на інших модулях
        # Для кожного модуля перевіряємо, чи сумарне допустиме навантаження на доступних модулях не менше
        # його номінального навантаження
        for key in table_of_redistribution.keys():
            if sum(
                    self._load_table[key]['redistributions'][target] for target in table_of_redistribution[key]
            ) < self._load_table[key]['nominal_load']:
                return False

        # Ініціалізація словника, що відслідковує поточне навантаження для кожного відмовленого модуля
        current_load = {key: self._load_table[key]['nominal_load'] for key in table_of_redistribution.keys()}

        # Початковий перерозподіл: навантаження на унікальні замінні модулі
        # Унікальні заміни - це ті, які є єдиною можливістю перерозподілу для конкретного модуля, що відмовив
        unique_alternatives = {}
        for key in table_of_redistribution.keys():
            unique_alternatives[key] = table_of_redistribution[key]
            for temp_key in table_of_redistribution.keys():
                if temp_key != key:
                    unique_alternatives[key] -= table_of_redistribution[temp_key]

        # Перерозподіл навантаження на унікальні модулі
        for key in table_of_redistribution.keys():
            for target in unique_alternatives[key]:
                current_load[key] -= min(
                    self._load_table[target]['max_load'] - self._load_table[target]['nominal_load'],
                    self._load_table[key]['redistributions'][target]
                )

        # Перевірка: чи вдалося повністю розподілити навантаження серед унікальних альтернатив
        if all(current_load[key] <= 0 for key in current_load.keys()):
            return True

        # Видаляємо зі списку перерозподілу ті модулі, які вже повністю компенсували своє навантаження
        for key in interesting_modules:
            if current_load[key] <= 0:
                current_load.pop(key, None)
                table_of_redistribution.pop(key, None)

        # Якщо залишився лише один модуль, що потребує компенсації, то достатньо можливостей для
        # розподілу, повертаємо True
        if len(current_load) <= 1:
            return True

        # Оцінюємо загальну можливість для компенсації - визначаємо максимальне доступне навантаження на всіх
        # працездатних модулях
        current_possibilities = {key: self._load_table[key]['max_load'] - self._load_table[key]['nominal_load']
                                 for key in self._load_table.keys() if key not in interesting_modules}

        # Видаляємо можливості для тих модулів, які не можуть допомогти жодному відмовленому модулю
        for key in list(current_possibilities.keys()):
            found = False
            for failed in current_load.keys():
                for target in table_of_redistribution[failed]:
                    if target == key:
                        found = True
            if not found:
                current_possibilities.pop(key, None)

        # Перевірка: чи можливостей на працюючих модулях достатньо для покриття сумарного
        # навантаження відмовлених модулів
        if sum(current_load.values()) > sum(current_possibilities.values()):
            return False

        # Якщо всі перевірки пройдені, перерозподіл навантаження можливий
        return True

    def _add_new_bad_state(self, bad_states, count_of_failures, count_of_elements):
        count_of_bad_states = len(bad_states)
        while len(bad_states) == count_of_bad_states:
            zero_positions = frozenset()
            while len(zero_positions) != count_of_failures:
                zero_positions = frozenset(
                    int(random.uniform(0, count_of_elements)) for i in range(count_of_failures)
                )
            bad_states.add(zero_positions)
        return zero_positions
