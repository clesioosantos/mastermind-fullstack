from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


SQLITE_COLUMN_PATCHES = {
    "users": {
        "best_score": "ALTER TABLE users ADD COLUMN best_score INTEGER NOT NULL DEFAULT 0",
    },
    "games": {
        "final_score": "ALTER TABLE games ADD COLUMN final_score INTEGER NOT NULL DEFAULT 0",
        "duration_seconds": "ALTER TABLE games ADD COLUMN duration_seconds INTEGER NOT NULL DEFAULT 0",
        "finished_at": "ALTER TABLE games ADD COLUMN finished_at DATETIME",
    },
}


def bootstrap_database(engine: Engine) -> None:
    if engine.dialect.name != "sqlite":
        return

    inspector = inspect(engine)

    with engine.begin() as connection:
        for table_name, columns in SQLITE_COLUMN_PATCHES.items():
            if not inspector.has_table(table_name):
                continue

            existing_columns = {
                column["name"] for column in inspector.get_columns(table_name)
            }

            for column_name, statement in columns.items():
                if column_name in existing_columns:
                    continue

                connection.execute(text(statement))
