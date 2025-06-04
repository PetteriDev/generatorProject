from scrapers import cramo, ramirent
import db

def main():
    run_id = db.get_next_run_id()
    print(f"Run ID: {run_id}")

    cramo_titles = cramo.get_cramo_titles()
    ramirent_titles = ramirent.get_ramirent_titles()

    if cramo_titles:
        db.insert_titles("cramo_generators", cramo_titles, run_id)
    else:
        print("No titles scraped from Cramo.")

    if ramirent_titles:
        db.insert_titles("ramirent_generators", ramirent_titles, run_id)
    else:
        print("No titles scraped from Ramirent.")

    print(f"Inserted {len(cramo_titles)} Cramo titles and {len(ramirent_titles)} Ramirent titles into the database.")

if __name__ == "__main__":
    main()
