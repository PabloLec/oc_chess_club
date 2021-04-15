from pathlib import Path

import mkdocs_gen_files

for path in Path("oc_chess_club").glob("**/*.py"):
    doc_path = Path("reference", path.relative_to("oc_chess_club")).with_suffix(".md")

    with mkdocs_gen_files.open(doc_path, "w") as f:
        ident = ".".join(path.relative_to("oc_chess_club").with_suffix("").parts)
        if ident[:2] == "__":
            continue
        print("::: " + ident, file=f)

    mkdocs_gen_files.set_edit_path(doc_path, Path("..", path))
