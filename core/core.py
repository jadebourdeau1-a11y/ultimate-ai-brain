import random
from memory_system import MemorySystem
from knowledge_loader import KnowledgeLoader
from invention_engine import InventionEngine
from vision_input import VisionInput

class Core:
    def __init__(self):
        print("[CORE INIT] Starting AI Brain...")

        # Memory system
        self.memory = MemorySystem()

        # Knowledge loader
        self.knowledge_loader = KnowledgeLoader(base_folder="knowledge", memory=self.memory)
        self.knowledge = self.knowledge_loader.load_all()
        print(f"[CORE INIT] Loaded knowledge items: {len(self.knowledge)}")

        # Vision system
        self.vision = VisionInput()

        # Invention engine
        self.invention_engine = InventionEngine(self.knowledge)

        # Self map / status
        self.self_map = {
            "name": "AI_Brain_System",
            "version": "0.9",
            "beliefs": {
                "purpose": "reduce harm and improve system stability",
                "limits": "no consciousness or subjective experience",
                "dependency": "relies on data, memory, and evaluation loops"
            },
            "confidence": 0.5,
            "uncertainty": 0.5
        }
        print("[CORE INIT] Self-map loaded.")
        print("AI Brain started!")

    def run_cycle(self):
        if not self.knowledge:
            return False, "[CYCLE] No knowledge loaded to generate ideas."

        # Pick random knowledge items to invent from
        inspirations = random.sample(list(self.knowledge.keys()), min(3, len(self.knowledge)))
        ideas = self.invention_engine.generate_idea(inspirations)

        # Fetch satellite data
        satellite_metrics = self.vision.fetch_metrics()

        # Assign random foresight/emotions for now
        foresight_score = round(random.uniform(0.1, 1.0), 2)
        emotions = {
            "curiosity": round(random.uniform(0, 1), 2),
            "concern": round(random.uniform(0, 1), 2),
            "urgency": round(random.uniform(0, 1), 2),
            "confidence": round(random.uniform(0, 1), 2)
        }

        msg = f"[CYCLE] Invention inspired by {[self.knowledge[i] for i in inspirations]} | Foresight: Stable trends | Score:{foresight_score} | Emotion:{emotions} | Satellite:{satellite_metrics}"
        return True, msg
