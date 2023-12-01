import numpy as np
from collections import *
class LifeGame(object):
    def __init__(self, initial_map: list[list[int]]):
        self.map = np.array(initial_map)
        self.shape = len(initial_map), len(initial_map[0])
        self.directions = [(0, 1),(0, -1),(1, 0),(-1, 0),(1, 1),(1, -1),(-1, 1),(-1, -1)]
        self.entities = {
            "fish": 10,
            "died_fish": 11,
            "shrimp": 15,
            "died_shrimp": 16,
            "rock": 5,
            "empty": 0,
        }
        self.idx_to_entity_idx = {
            10: "fish",
            11: "died_fish",
            15: "shrimp",
            16: "died_shrimp",
            5: "rock",
            0: "empty",
        }
    def _get_neighbors(self, i: int, j: int) -> Counter[str]:
        neighbors: Counter[str] = Counter()
        for di, dj in self.directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.shape[0] and 0 <= nj < self.shape[1]:
                entity_idx=self.idx_to_entity_idx.get(self.map[ni][nj], "new_entity_idx")
                neighbors[entity_idx] += 1
            else: neighbors["empty"] += 1
        return neighbors
    def _update_map(self) -> None:
        self.map *= 5
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                entity_idx=self.map[i][j]
                entity_name=self.idx_to_entity_idx[entity_idx]
                neighbors = self._get_neighbors(i, j)
                if entity_name == "fish" or entity_name == "shrimp":
                    neighbors_like_entity_idx = (neighbors[entity_name] + neighbors[f"died_{entity_name}"])
                    if neighbors_like_entity_idx >= 4 or neighbors_like_entity_idx <= 1: self.map[i][j] += 1
                elif entity_idx == self.entities["empty"]:
                    if neighbors["fish"] + neighbors["died_fish"] == 3:
                        self.map[i][j] = (self.entities["fish"] // 5 + 5) * 5
                    elif neighbors["shrimp"] + neighbors["died_shrimp"] == 3:
                        self.map[i][j] = (self.entities["shrimp"] // 5 + 5) * 5
        self.map[(self.map % 5)==1]=0
        self.map = (self.map // 5) % 5
    def get_next_generation(self) -> list[list[int]]:
        self._update_map()
        return self.map.tolist()