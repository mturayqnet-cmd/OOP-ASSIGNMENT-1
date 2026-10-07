import sys

from models import Citizen, Complaint
from registry import (add_complaint, display_all, find_complaint,
                      display_summary)


def run_demo():
    registry = {}  # the single dictionary: complaint_id -> Complaint

    print("===, Citizen Complaint System ===\n")

    # 1. Object creation
    citizen_a = Citizen("Western Area Urban")
    citizen_b = Citizen("Bo")
    citizen_a.display_info()
    citizen_b.display_info()
    print()

    # 2. Objects interacting: a Citizen files Complaints
    c1 = citizen_a.file_complaint("Water Supply",
                                  "No running water in our street for 5 days.")
    c2 = citizen_b.file_complaint("Roads",
                                  "Large potholes near the main market.")
    c3 = Complaint.from_text(citizen_a,
                             "Waste Management | Rubbish not collected this week.")

    # 3. Add records to the dictionary
    for complaint in (c1, c2, c3):
        add_complaint(registry, complaint)
    print()

    # 4. Display records
    display_all(registry)

    # 5. Update status (instance method)
    c1.update_status("Under Review")
    c1.update_status("Resolved")
    print("After updates:")
    c1.display_info()
    print()

    # 6. Business rule: status cannot go backwards
    try:
        c1.update_status("Received")
    except ValueError as error:
        print(f"Blocked as expected -> {error}")

    # 7. Privacy rule: personal data is rejected
    try:
        citizen_b.file_complaint("Other", "Call me on 076123456 please.")
    except ValueError as error:
        print(f"Privacy guard -> {error}")
    print()

    # 8. Class methods and summary
    print(f"Citizens registered: {Citizen.total_registered()}")
    print(f"Complaints filed   : {Complaint.total_filed()}")
    display_summary(registry)


def choose_district():
    print("\nSelect your district:")
    for number, name in enumerate(Citizen.DISTRICTS, start=1):
        print(f"  {number:>2}. {name}")
    choice = input("Number: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(Citizen.DISTRICTS):
        return Citizen.DISTRICTS[int(choice) - 1]
    return None


def choose_category():
    print("\nSelect a category:")
    for number, name in enumerate(Complaint.CATEGORIES, start=1):
        print(f"  {number}. {name}")
    choice = input("Number: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(Complaint.CATEGORIES):
        return Complaint.CATEGORIES[int(choice) - 1]
    return None


def run_menu():
    registry = {}
    citizen = None

    while True:
        print("\n===== CITIZEN COMPLAINT SYSTEM =====")
        print("1. Start as a new anonymous citizen")
        print("2. File a complaint")
        print("3. View all complaints")
        print("4. Update complaint status")
        print("5. Summary")
        print("0. Exit")
        option = input("Choose: ").strip()

        if option == "1":
            district = choose_district()
            if district is None:
                print("Invalid choice.")
                continue
            citizen = Citizen(district)
            print(f"Your anonymous reference: {citizen.reference}")

        elif option == "2":
            if citizen is None:
                print("Please start as a citizen first (option 1).")
                continue
            category = choose_category()
            if category is None:
                print("Invalid choice.")
                continue
            description = input("Describe the problem (no phone/email): ")
            try:
                complaint = citizen.file_complaint(category, description)
                add_complaint(registry, complaint)
            except ValueError as error:
                print(f"Could not file complaint: {error}")

        elif option == "3":
            display_all(registry)

        elif option == "4":
            complaint = find_complaint(registry, input("Complaint ID: ").strip())
            if complaint is None:
                print("Complaint not found.")
                continue
            print("Stages:", " > ".join(Complaint.STATUS_FLOW))
            try:
                complaint.update_status(input("New status: ").strip())
                print("Status updated.")
            except ValueError as error:
                print(f"Could not update: {error}")

        elif option == "5":
            display_summary(registry)

        elif option == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == "demo":
        run_demo()
    else:
        run_menu()
