import frappe
from frappe.model.document import Document

class Agency(Document):

    def validate(self):
        self.validate_active_status()
        self.validate_agency_items()

    def validate_active_status(self):
        if not self.is_active and self.items:
            frappe.throw(
                "Cannot deactivate Agency while Agency Items exist. Please remove items first."
            )

    def validate_agency_items(self):
        seen_items = set()

        for row in self.items:
            if row.min_order_qty <= 0:
                frappe.throw(
                    f"Row {row.idx}: Minimum Order Quantity must be greater than 0"
                )

            if row.lead_time_days < 0:
                frappe.throw(
                    f"Row {row.idx}: Lead Time (Days) cannot be negative"
                )

            if row.item_code in seen_items:
                frappe.throw(
                    f"Row {row.idx}: Item {row.item_code} is duplicated in Agency Items"
                )

            seen_items.add(row.item_code)
            

@frappe.whitelist()
def create_supplier(agency):
    agency_doc = frappe.get_doc("Agency", agency)

    if frappe.db.exists("Supplier", agency_doc.agency_name):
        frappe.throw("Supplier already exists.")

    supplier = frappe.new_doc("Supplier")
    supplier.supplier_name = agency_doc.agency_name
    supplier.supplier_type = "Company"
    supplier.save(ignore_permissions=True)

    frappe.msgprint(
        f"Supplier <b>{supplier.name}</b> created successfully."
    )

    return supplier.name
