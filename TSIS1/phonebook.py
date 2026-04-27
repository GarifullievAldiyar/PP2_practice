import psycopg2
import json
import csv

from config import load_config



def connect():
    config = load_config()
    return psycopg2.connect(**config)



def add_contact(cur):
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group: ")

    cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
    g = cur.fetchone()

    if g is None:
        cur.execute("INSERT INTO groups(name) VALUES(%s) RETURNING id", (group,))
        gid = cur.fetchone()[0]
    else:
        gid = g[0]

    cur.execute("""
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (name, email, birthday, gid))

    cid = cur.fetchone()[0]

    while True:
        phone = input("Phone (or empty to stop): ")
        if not phone:
            break
        ptype = input("Type (home/work/mobile): ")

        cur.execute("""
            INSERT INTO phones(contact_id, phone, type)
            VALUES (%s, %s, %s)
        """, (cid, phone, ptype))


def show_all(cur):
    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY c.name
    """)

    for row in cur.fetchall():
        print(row)



def filter_group(cur):
    g = input("Group: ")

    cur.execute("""
        SELECT c.name, c.email
        FROM contacts c
        JOIN groups gr ON c.group_id = gr.id
        WHERE gr.name=%s
    """, (g,))

    print(cur.fetchall())


def search_email(cur):
    q = input("Email search: ")

    cur.execute("""
        SELECT name, email
        FROM contacts
        WHERE email ILIKE %s
    """, (f"%{q}%",))

    print(cur.fetchall())


def search_all(cur):
    q = input("Search: ")

    cur.execute("SELECT * FROM search_contacts(%s)", (q,))
    print(cur.fetchall())



def sort_contacts(cur):
    allowed = ["name", "birthday"]
    s = input("Sort by (name/birthday): ")

    if s not in allowed:
        print("Invalid field")
        return

    cur.execute(f"""
        SELECT name, email, birthday
        FROM contacts
        ORDER BY {s}
    """)

    print(cur.fetchall())



def paginate(cur):
    limit = 5
    offset = 0

    while True:
        cur.execute("""
            SELECT name, email
            FROM contacts
            ORDER BY name
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()

        print("\n--- PAGE ---")
        for r in rows:
            print(r)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        elif cmd == "quit":
            break



def export_json(cur):
    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
    """)

    data = cur.fetchall()

    with open("contacts.json", "w") as f:
        json.dump(data, f, default=str, indent=4)

    print("Exported to contacts.json")


def import_json(cur, conn):
    with open("contacts.json") as f:
        data = json.load(f)

    for row in data:
        name, email, birthday, group, phone, ptype = row

        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        existing = cur.fetchone()

        if existing:
            choice = input(f"{name} exists (skip/overwrite): ")

            if choice == "skip":
                continue
            elif choice == "overwrite":
                cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

        cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
        g = cur.fetchone()

        if not g:
            cur.execute("INSERT INTO groups(name) VALUES(%s) RETURNING id", (group,))
            gid = cur.fetchone()[0]
        else:
            gid = g[0]

        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (name, email, birthday, gid))

        cid = cur.fetchone()[0]

        if phone:
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (cid, phone, ptype))

    conn.commit()
    print("Imported JSON")



def import_csv(cur, conn):
    file = input("CSV filename: ")

    with open(file) as f:
        reader = csv.DictReader(f)

        for row in reader:
            cur.execute("""
                INSERT INTO contacts(name, email, birthday)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (row["name"], row["email"], row["birthday"]))

            cid = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (cid, row["phone"], row["type"]))

    conn.commit()
    print("CSV imported")



def add_phone_proc(cur):
    name = input("Name: ")
    phone = input("Phone: ")
    ptype = input("Type: ")

    cur.execute("CALL add_phone(%s,%s,%s)", (name, phone, ptype))


def move_group_proc(cur):
    name = input("Name: ")
    group = input("New group: ")

    cur.execute("CALL move_to_group(%s,%s)", (name, group))



def menu():
    conn = connect()
    cur = conn.cursor()

    while True:
        print("""
1. Add contact
2. Show all
3. Filter by group
4. Search email
5. Search all
6. Sort
7. Pagination
8. Export JSON
9. Import JSON
10. Import CSV
11. Add phone (proc)
12. Move group (proc)
0. Exit
""")

        choice = input("Choice: ")

        try:
            if choice == "1":
                add_contact(cur)
            elif choice == "2":
                show_all(cur)
            elif choice == "3":
                filter_group(cur)
            elif choice == "4":
                search_email(cur)
            elif choice == "5":
                search_all(cur)
            elif choice == "6":
                sort_contacts(cur)
            elif choice == "7":
                paginate(cur)
            elif choice == "8":
                export_json(cur)
            elif choice == "9":
                import_json(cur, conn)
            elif choice == "10":
                import_csv(cur, conn)
            elif choice == "11":
                add_phone_proc(cur)
            elif choice == "12":
                move_group_proc(cur)
            elif choice == "0":
                break

            conn.commit()

        except Exception as e:
            conn.rollback()
            print("Error:", e)

    cur.close()
    conn.close()


if __name__ == "__main__":
    menu()