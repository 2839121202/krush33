import sqlite3


def init_db():
    conn = sqlite3.connect("predictions.db")
    c = conn.cursor()

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS prediction_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            predicted_disease TEXT NOT NULL,
            actual_disease TEXT NOT NULL,
            comments TEXT,
            image_path TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
