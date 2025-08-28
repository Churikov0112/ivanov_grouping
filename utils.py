import csv
import matplotlib.pyplot as plt
import networkx as nx

def export_groups_to_csv(groups, filename="groups.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Группа", "Участники"])
        for i, group in enumerate(groups):
            members = ", ".join(str(u) for u in group)
            writer.writerow([f"Группа {i+1}", members])

def visualize_groups(groups):
    G = nx.Graph()
    for i, group in enumerate(groups):
        for user in group:
            G.add_node(user.id + 1, group=i)
        for j in range(len(group)):
            for k in range(j + 1, len(group)):
                G.add_edge(group[j].id + 1, group[k].id + 1)

    pos = nx.spring_layout(G)
    colors = [G.nodes[n]['group'] for n in G.nodes]
    nx.draw(G, pos, with_labels=True, node_color=colors, cmap=plt.cm.Set3, node_size=600, font_size=10)
    plt.title("Группы пользователей")
    plt.show()