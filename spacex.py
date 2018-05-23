from collections import OrderedDict
import os
import requests
import matplotlib.pyplot as plt
import csv


# Payload mass statistics
def get_years_mass_data(url):
    req = requests.get(url)
    data = req.json()

    years_mass = {}
    for flight in data:
        payload_mass = flight['rocket']['second_stage']['payloads'][0]['payload_mass_kg']
        if payload_mass is None:
            continue
        years_mass[flight['launch_year']] = years_mass.get(flight['launch_year'], 0) + payload_mass

    return years_mass


# Saving to CSV
def save_to_csv(data, file_name):
    file_path = './Csv_Files/'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(file_path + file_name + '.csv', 'w') as csv_file:
        w = csv.writer(csv_file)
        w.writerows(data.items())


# Plotting and saving graph
def plot_graph(data, graph_name, show=False):
    graph_path = './Graphs/'
    plt.barh(range(len(data)), list(data.values()), align='center', alpha=0.5)
    plt.margins(0.15, 0)
    plt.yticks(range(len(data)), list(data.keys()))
    plt.xlabel('Total payload mass [kg]')
    plt.ylabel('Year')
    plt.title('Statistics of payload mass carried by SpaceX rockets')
    for y, x in enumerate(data.values()):
        plt.text(x, y - 0.1, str(x), color='blue', fontsize=9)
    if not os.path.exists(graph_path):
        os.makedirs(graph_path)
    plt.savefig(graph_path + graph_name + '.png')
    if show:
        plt.show()


def main():
    years_mass = get_years_mass_data('https://api.spacexdata.com/v2/launches')
    save_to_csv(years_mass, 'years_mass')
    plot_graph(OrderedDict(sorted(years_mass.items(), reverse=True)), 'years_mass_graph', show=True)


if __name__ == "__main__":
    main()
