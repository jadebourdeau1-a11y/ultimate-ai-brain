import json
import os

class KnowledgeLoader:
    def __init__(self, folder="knowledge"):
        self.folder = folder

    def load_all(self):
        knowledge = {}
        if not os.path.exists(self.folder):
            return knowledge

        for file in os.listdir(self.folder):
            if file.endswith(".json"):
                path = os.path.join(self.folder, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        knowledge[file] = json.load(f)
                except Exception:
                    continue
        return knowledge

class Memory:
    def __init__(self, memory_file="memory.json"):
        self.memory_file = memory_file
        self.data = []
        self._load()

    def _load(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = []

    def store(self, item):
        self.data.append(item)
        self._save()

    def retrieve_last(self, limit=5, data_type=None):
        filtered = self.data
        if data_type:
            filtered = [d for d in self.data if d.get("type") == data_type]
        return filtered[-limit:]

    def _save(self):
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)
