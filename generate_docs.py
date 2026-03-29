import inspect
import pawpal_system

OUTPUT_PATH = "docs/api.md"

classes = [pawpal_system.Task, pawpal_system.Schedule, pawpal_system.Owner, pawpal_system.Pet]

lines = ["# PawPal System API Documentation\n"]

for cls in classes:
    lines.append(f"## {cls.__name__}\n")
    if cls.__doc__:
        lines.append(cls.__doc__.strip() + "\n")
    for name, func in inspect.getmembers(cls, predicate=inspect.isfunction):
        if name.startswith("__"):
            continue
        sig = inspect.signature(func)
        doc = inspect.getdoc(func) or "No docstring."
        lines.append(f"### {name}{sig}\n")
        lines.append(doc + "\n")
    lines.append("---\n")

# create output folder if needed
import os
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Documentation generated to {OUTPUT_PATH}")
