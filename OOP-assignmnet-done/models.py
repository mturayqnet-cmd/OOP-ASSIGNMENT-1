import re
from datetime import date


class Citizen:
    """An anonymous citizen who can file complaints."""

    # Tuple: fixed, read-only list of Sierra Leone's 16 districts.
    DISTRICTS = (
        "Bo", "Bombali", "Bonthe", "Falaba", "Kailahun", "Kambia",
        "Karene", "Kenema", "Koinadugu", "Kono", "Moyamba", "Port Loko",
        "Pujehun", "Tonkolili", "Western Area Rural", "Western Area Urban",
    )

    _next_number = 1  # class attribute shared by all citizens

    def __init__(self, district):
        if district not in Citizen.DISTRICTS:
            raise ValueError(f"Unknown district: {district}")
        self.reference = f"CIT-{Citizen._next_number:04d}"
        Citizen._next_number += 1
        self.district = district
        self.complaints_filed = 0

    # ---- instance methods ----
    def file_complaint(self, category, description):
        """Create a Complaint object linked to this citizen."""
        complaint = Complaint(self, category, description)
        self.complaints_filed += 1
        return complaint

    def display_info(self):
        print(f"Citizen {self.reference} | District: {self.district} "
              f"| Complaints filed: {self.complaints_filed}")

    # ---- class method ----
    @classmethod
    def total_registered(cls):
        """How many anonymous citizens have been created so far."""
        return cls._next_number - 1


class Complaint:
    """A complaint filed by a Citizen about a public service."""

    # Tuples: fixed values that should never change while the program runs.
    CATEGORIES = (
        "Water Supply", "Electricity", "Roads", "Health Services",
        "Education", "Waste Management", "Corruption", "Other",
    )
    STATUS_FLOW = ("Received", "Under Review", "In Progress", "Resolved")

    _next_number = 1  # class attribute used to generate unique IDs

    def __init__(self, citizen, category, description, filed_on=None):
        if not Complaint.is_valid_category(category):
            raise ValueError(f"Invalid category: {category}")
        if not description or not description.strip():
            raise ValueError("Description cannot be empty.")
        if Complaint.contains_personal_data(description):
            raise ValueError(
                "Description looks like it contains personal data "
                "(phone number or email). Please remove it - this system "
                "does not store personal information."
            )

        self.complaint_id = f"CMP-{Complaint._next_number:04d}"
        Complaint._next_number += 1

        self.citizen = citizen              # object interaction: Complaint -> Citizen
        self.category = category
        self.description = description.strip()
        self.status = Complaint.STATUS_FLOW[0]

        # Tuple (day, month, year) for the filing date
        if filed_on is None:
            today = date.today()
            filed_on = (today.day, today.month, today.year)
        self.filed_on = filed_on

    # ---- instance methods ----
    def update_status(self, new_status):
        """Move the complaint forward in the workflow (never backwards)."""
        if new_status not in Complaint.STATUS_FLOW:
            raise ValueError(f"Invalid status: {new_status}")
        current = Complaint.STATUS_FLOW.index(self.status)
        target = Complaint.STATUS_FLOW.index(new_status)
        if target <= current:
            raise ValueError(
                f"Cannot move from '{self.status}' to '{new_status}'."
            )
        self.status = new_status

    def is_resolved(self):
        return self.status == Complaint.STATUS_FLOW[-1]

    def display_info(self):
        day, month, year = self.filed_on  # tuple unpacking
        print(f"[{self.complaint_id}] {self.category} | Status: {self.status}")
        print(f"    Filed by: {self.citizen.reference} "
              f"({self.citizen.district}) on {day:02d}/{month:02d}/{year}")
        print(f"    Details : {self.description}")

    # ---- class methods ----
    @classmethod
    def from_text(cls, citizen, text):
        """Build a complaint from a single line: 'Category | description'."""
        if "|" not in text:
            raise ValueError("Use the format: Category | description")
        category, description = text.split("|", 1)
        return cls(citizen, category.strip(), description)

    @classmethod
    def total_filed(cls):
        """How many complaints have been created so far."""
        return cls._next_number - 1

    # ---- static methods (no access to self or cls needed) ----
    @staticmethod
    def is_valid_category(category):
        return category in Complaint.CATEGORIES

    @staticmethod
    def contains_personal_data(text):
        """Privacy guard: detect phone-number-like digits or email addresses."""
        has_phone = re.search(r"\d{7,}", text.replace(" ", "").replace("-", ""))
        has_email = re.search(r"\S+@\S+\.\S+", text)
        return bool(has_phone or has_email)
