states_needed = set(['北京', '上海', '广州', '深圳', '杭州', '南京', '石家庄', '银川'])

stations = {}
stations['kone'] = set(['北京', '上海', '广州'])
stations['ktwo'] = set(['北京''杭州', '南京'])
stations['kthree'] = set(['广州', '深圳', '杭州'])
stations['kfour'] = set(['北京', '银川'])
stations['kfive'] = set(['石家庄', '银川'])

final_stations = set()

while states_needed:
    best_station = None
    states_covered = set()
    for station, states in stations.items():
        covered = states_needed & states
        if len(covered) > len(states_covered):
                best_station = station
                states_covered = covered

    states_needed -= states_covered
    final_stations.add(best_station)

print(final_stations)