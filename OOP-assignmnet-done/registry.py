from models import Complaint
def add_complaint(registry, complaint):
    """Add a Complaint object to the registry dictionary."""
    registry[complaint.complaint_id] = complaint
    print(f"Complaint {complaint.complaint_id} saved.")
def display_all(registry):
    """Loop through the dictionary and display every complaint."""
    if not registry:
        print("No complaints recorded yet.")
        return
    for complaint_id, complaint in registry.items():
        complaint.display_info()
        print()


def find_complaint(registry, complaint_id):
    """Return the Complaint with this ID, or None if it does not exist."""
    return registry.get(complaint_id.upper())


def display_summary(registry):
    """Show how many complaints are at each stage of the workflow."""
    print(f"Total complaints: {len(registry)}")
    for status in Complaint.STATUS_FLOW:
        count = sum(1 for c in registry.values() if c.status == status)
        print(f"  {status:<13}: {count}")
