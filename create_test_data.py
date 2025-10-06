import psycopg2
from datetime import datetime
import os

try:
    # Database connection
    conn = psycopg2.connect(
        host="localhost",
        database="CattleTrackingDB",
        user="postgres",
        password="123456"
    )
    cur = conn.cursor()

    print("Connected to database successfully")

    # Insert 10 animals directly for farm ID 7 (Entre Rios - Vaca GPS)
    animals_data = [
        ('Vaca Entre Rios 01', 'ER001', 'Female', 'Holstein', '2021-03-15', 450.0, 4),
        ('Vaca Entre Rios 02', 'ER002', 'Male', 'Angus', '2020-08-22', 520.0, 6),
        ('Vaca Entre Rios 03', 'ER003', 'Female', 'Holstein', '2021-05-10', 420.0, 7),
        ('Vaca Entre Rios 04', 'ER004', 'Female', 'Brahman', '2020-12-05', 480.0, 8),
        ('Vaca Entre Rios 05', 'ER005', 'Male', 'Angus', '2021-01-18', 510.0, 9),
        ('Vaca Entre Rios 06', 'ER006', 'Female', 'Holstein', '2021-04-25', 440.0, 10),
        ('Vaca Entre Rios 07', 'ER007', 'Male', 'Hereford', '2020-09-12', 495.0, 11),
        ('Vaca Entre Rios 08', 'ER008', 'Female', 'Holstein', '2021-06-08', 415.0, 12),
        ('Vaca Entre Rios 09', 'ER009', 'Female', 'Brahman', '2020-11-30', 465.0, 13),
        ('Vaca Entre Rios 10', 'ER010', 'Male', 'Angus', '2021-02-14', 505.0, 14)
    ]

    for name, tag, gender, breed, birth_date, weight, tracker_id in animals_data:
        try:
            cur.execute("""
                INSERT INTO "Animals" ("Name", "Tag", "Gender", "Breed", "BirthDate", "Weight", "Status", "FarmId", "TrackerId", "CreatedAt", "UpdatedAt")
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT ("Tag") DO UPDATE SET
                    "TrackerId" = EXCLUDED."TrackerId",
                    "FarmId" = EXCLUDED."FarmId",
                    "UpdatedAt" = NOW()
            """, (name, tag, gender, breed, birth_date, weight, 'Active', 7, tracker_id, datetime.now(), datetime.now()))
            print(f"OK Created/Updated animal {tag} - {name} with tracker ID {tracker_id}")
        except Exception as e:
            print(f"ERROR Failed to create animal {tag}: {str(e)}")

    conn.commit()
    print("Changes committed successfully")

    # Verify the results
    cur.execute("""
        SELECT
            a."Tag",
            a."Name",
            t."DeviceId",
            a."TrackerId",
            f."Name" as FarmName
        FROM "Animals" a
        JOIN "Trackers" t ON a."TrackerId" = t."Id"
        JOIN "Farms" f ON a."FarmId" = f."Id"
        WHERE f."Id" = 7
        ORDER BY a."Tag"
    """)

    results = cur.fetchall()
    print(f"\nVerification: Found {len(results)} animals in farm 'Entre Rios - Vaca GPS':")
    for tag, name, device_id, tracker_id, farm_name in results:
        print(f"  - {tag}: {name} -> Tracker {device_id} (ID: {tracker_id})")

    cur.close()
    conn.close()
    print("\nDatabase setup complete!")

except Exception as e:
    print(f"Database connection error: {str(e)}")
    print("Make sure PostgreSQL is running and credentials are correct")