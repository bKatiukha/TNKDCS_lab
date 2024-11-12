import matplotlib.pyplot as plt

import data
import operator
import operability_functions
from ReliabilityCalculator import ReliabilityCalculator


def visualize_errors_chart(data, title):
    elements_without_active_failover = sorted(data.items(), key=operator.itemgetter(1))
    error_types, counts = zip(*elements_without_active_failover)
    total_errors = sum(counts)

    # Plotting the bar chart
    plt.figure(figsize=(12, 6))
    bars = plt.bar(error_types, counts, color='skyblue')
    plt.xlabel('Error Types')
    plt.ylabel('Error Counts')
    plt.title(title)

    # Add total errors count to the top of the chart
    plt.text(0.5, 0.9, f'Total Errors: {total_errors}', ha='center', va='center',
             transform=plt.gca().transAxes, fontsize=14, color='darkblue', fontweight='bold')

    # Add numeric labels on top of each bar
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                 str(count), ha='center', va='bottom', fontsize=10, color='black', fontweight='bold')

    plt.xticks(rotation=45, ha='right')  # Rotate labels for better readability
    plt.tight_layout()  # Adjust layout to prevent label cutoff

    # Display the plot
    plt.show()


def print_result(calculator, use_active_failover=False):
    use_active_failover_title = 'з активною відмовостійкістю' if use_active_failover else ''
    probability_without_active_failover = calculator.calculate_reliability(use_active_failover)
    print(f'\n\nРезультати розрахунків {use_active_failover_title}')
    for index, reliability in enumerate(calculator._reliabilities):
        print(f'{index} помилок {use_active_failover_title}: {reliability}')
    print(f'Загальна надійність системи {use_active_failover_title} {probability_without_active_failover}')

    chart_title = 'Errors ' + use_active_failover_title
    visualize_errors_chart(calculator._statistics, chart_title)


def print_improvement_probabilities(probability, mod_probability, label):
    mod_probability_result = ((1 - probability - (1 - mod_probability)) / (1 - mod_probability) * 100)
    mod_probability_result1 = (1 - probability) / (1 - mod_probability)

    print(f'зменшення непрацездатності системи {label} на {mod_probability_result} %')
    print(f'зменшення непрацездатності системи {label} в {mod_probability_result1} рази')


if __name__ == '__main__':
    calculator = ReliabilityCalculator(
        data.elements,
        operability_functions.logical_structure_function,
        data.load_table
    )
    #
    probability_without_active_failover = calculator.calculate_reliability()
    print_result(calculator, False)

    probability_with_active_failover = calculator.calculate_reliability(use_active_failover=True)
    print_result(calculator, True)

    #
    calculator_mod = ReliabilityCalculator(
        data.elements,
        operability_functions.logical_structure_function_mod,
        data.load_table
    )

    mod_probability_without_active_failover = calculator_mod.calculate_reliability()
    print_result(calculator_mod, False)
    print_improvement_probabilities(probability_without_active_failover, mod_probability_without_active_failover, 'mod1')

    mod_probability_with_active_failover = calculator_mod.calculate_reliability(use_active_failover=True)
    print_result(calculator_mod, True)
    print_improvement_probabilities(probability_with_active_failover, mod_probability_with_active_failover, 'mod1')

    #
    calculator_mod2 = ReliabilityCalculator(
        data.elements,
        operability_functions.logical_structure_function_mod2,
        data.load_table
    )

    mod2_probability_without_active_failover = calculator_mod2.calculate_reliability()
    print_result(calculator_mod2, False)
    print_improvement_probabilities(probability_without_active_failover, mod2_probability_without_active_failover, 'mod2')

    mod2_probability_with_active_failover = calculator_mod2.calculate_reliability(use_active_failover=True)
    print_result(calculator_mod2, True)
    print_improvement_probabilities(probability_with_active_failover, mod2_probability_with_active_failover, 'mod2')
