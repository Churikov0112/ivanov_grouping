import numpy as np

class User:
    def __init__(self, user_id, politics, adventure, income, tolerance, group_size, important_trait, flexible_trait):
        self.id = user_id
        self.traits = {
            "politics": politics,
            "adventure": adventure,
            "income": income,
            "tolerance": tolerance
        }
        self.group_size = max(group_size, 2)
        self.important_trait = important_trait
        self.flexible_trait = flexible_trait

    def __str__(self):
        return f"Пользователь {self.id + 1}"

class GroupMatcher:
    def __init__(self, users):
        self.users = users
        self.visited = set()
        self.groups = []

    def weighted_difference(self, user1, user2, important_trait):
        total_weight = 0
        diff = 0
        for trait in user1.traits:
            weight = 1.0 if trait == important_trait else 0.5
            total_weight += weight
            diff += weight * abs(user1.traits[trait] - user2.traits[trait])
        return diff / total_weight

    def match(self):
        for user in self.users:
            if user.id in self.visited:
                continue
            group = [user]
            self.visited.add(user.id)

            # Прямое совпадение
            for other in self.users:
                if other.id in self.visited or len(group) >= user.group_size:
                    continue
                diff = self.weighted_difference(user, other, user.important_trait)
                if diff < 0.2 and other.group_size >= len(group) + 1:
                    group.append(other)
                    self.visited.add(other.id)

            # Посредник
            if len(group) < user.group_size:
                best_mediator = None
                min_diff = float('inf')
                for mediator in self.users:
                    if mediator.id in self.visited:
                        continue
                    mediator_diff = self.weighted_difference(user, mediator, user.important_trait)
                    if mediator_diff < 0.2:
                        for other in self.users:
                            if other.id in self.visited or len(group) >= user.group_size:
                                continue
                            other_diff = abs(user.traits[mediator.flexible_trait] - other.traits[mediator.flexible_trait])
                            if other_diff < 0.4 and other.group_size >= len(group) + 1:
                                total_diff = mediator_diff + other_diff
                                if total_diff < min_diff:
                                    min_diff = total_diff
                                    best_mediator = other
                if best_mediator:
                    group.append(best_mediator)
                    self.visited.add(best_mediator.id)

            if len(group) > 1:
                self.groups.append(group)

        return self.groups
