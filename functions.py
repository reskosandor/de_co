

def color_sync(graph, agents, previous_agents, color, m):
    for key in color:
        for i in agents:
            if key == agents[i]:
                color[key] = "black"

    for key in color:
        if key in previous_agents.values() and key not in agents.values():
            color[key] = "white"

    if color[key] == "white":
        neighbours = [j for j in graph[key]]
        counter = 0
        for k in range(len(neighbours)):
            if color[(neighbours[k])] == "grey":
                counter = counter + 1
            if m <= counter:
                color[key] = "grey"
            elif counter < m:
                color[key] = "white"

def color_sync_with_error(graph, agents, previous_agents, color, m, backup_agents, previous_backup_agents):
    for key in color:
        for i in agents:
            if key == agents[i]:
                color[key] = "black"

    for key in color:
        for i in backup_agents:
            if key == backup_agents[i]:
                color[key] = "black"

    for key in color:
        if key in previous_agents.values() or key in previous_backup_agents:
            if key not in agents.valies() and key not in backup_agents.values():
                color[key] = "white"

    if color[key] == "white":
        neighbours = [j for j in graph[key]]
        counter = 0
        for k in range(len(neighbours)):
            if color[(neighbours[k])] == "grey":
                counter = counter + 1
            if m <= counter:
                color[key] = "grey"
            elif counter < m:
                color[key] = "white"

