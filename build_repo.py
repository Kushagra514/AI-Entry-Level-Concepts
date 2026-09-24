import os
import subprocess

repo_path = "."

dirs = [
    "00-foundations",
    "01-ml-basics",
    "02-deep-learning",
    "03-nlp",
    "04-computer-vision",
    "05-ml-ops",
    "06-system-design",
    "13-project-defense",
    "14-cheat-sheets",
    "15-mock-interviews",
    "16-dsa-foundations",
    "17-data-structures",
    "18-algorithms",
    "19-dp-deep-dive",
    "20-dsa-patterns",
    "21-oop-and-lld",
    "22-cs-fundamentals",
    "23-dsa-interview-questions",
    "24-dsa-mock-interviews"
]

for d in dirs:
    os.makedirs(os.path.join(repo_path, d), exist_ok=True)
