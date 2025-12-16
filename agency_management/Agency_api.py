import frappe


@frappe.whitelist()
def create_agency_from_payload(payload=None):
    """
    Creates:
    - Territory
    - Item Group
    - Items
    - Contact
    - Agency
    - Agency Items
    """

    # ----------------------------------------------------
    # HANDLE PAYLOAD (RPC + REST SAFE)
    # ----------------------------------------------------
    if not payload:
        payload = frappe.form_dict

    if isinstance(payload, str):
        payload = frappe.parse_json(payload)

    agency_data = payload.get("agency")
    items = payload.get("items", [])
    item_group = payload.get("item_group")

    if not agency_data:
        frappe.throw("Agency data is required")

    # ----------------------------------------------------
    # TERRITORY
    # ----------------------------------------------------
    territory = agency_data.get("territory")
    if territory and not frappe.db.exists("Territory", territory):
        frappe.get_doc({
            "doctype": "Territory",
            "territory_name": territory
        }).insert(ignore_permissions=True)

    # ----------------------------------------------------
    # ITEM GROUP
    # ----------------------------------------------------
    if item_group and not frappe.db.exists("Item Group", item_group):
        frappe.get_doc({
            "doctype": "Item Group",
            "item_group_name": item_group,
            "parent_item_group": "All Item Groups",
            "is_group": 0
        }).insert(ignore_permissions=True)

    # ----------------------------------------------------
    # ITEMS
    # ----------------------------------------------------
    for row in items:
        if not frappe.db.exists("Item", row["item_code"]):
            item = frappe.get_doc({
                "doctype": "Item",
                "item_code": row["item_code"],
                "item_name": row["item_name"],
                "item_group": item_group,
                "stock_uom": row.get("stock_uom", "Nos"),
                "is_stock_item": 1
            })
            item.insert(ignore_permissions=True)

            if row.get("valuation_rate"):
                frappe.db.set_value(
                    "Item",
                    row["item_code"],
                    "valuation_rate",
                    row["valuation_rate"]
                )

    # ----------------------------------------------------
    # CONTACT (CREATE FIRST – REQUIRED FOR LINK FIELD)
    # ----------------------------------------------------
    contact_name = None
    contact_email = agency_data.get("primary_contact_email")

    if contact_email:
        existing_contact = frappe.db.get_value(
            "Contact",
            {"email_id": contact_email},
            "name"
        )

        if existing_contact:
            contact_name = existing_contact
        else:
            contact = frappe.get_doc({
                "doctype": "Contact",
                "first_name": agency_data.get("primary_contact_name"),
                "email_id": contact_email,
                "mobile_no": agency_data.get("primary_contact_mobile")
            })
            contact.insert(ignore_permissions=True)
            contact_name = contact.name

    # ----------------------------------------------------
    # AGENCY
    # ----------------------------------------------------
    agency_name = agency_data["agency_name"]

    if frappe.db.exists("Agency", agency_name):
        frappe.throw(f"Agency '{agency_name}' already exists")

    agency = frappe.get_doc({
        "doctype": "Agency",
        "agency_name": agency_name,
        "territory": territory,
        "primary_contact": contact_name,
        "is_active": agency_data.get("is_active", 1)
    })

    # Agency Items (child table)
    for row in items:
        agency.append("items", {
            "item_code": row["item_code"],
            "min_order_qty": row["min_order_qty"],
            "lead_time_days": row["lead_time_days"]
        })

    agency.insert(ignore_permissions=True)
    

    # ----------------------------------------------------
    # LINK CONTACT → AGENCY
    # ----------------------------------------------------
    if contact_name:
        contact = frappe.get_doc("Contact", contact_name)
        contact.append("links", {
            "link_doctype": "Agency",
            "link_name": agency.name
        })
        contact.save(ignore_permissions=True)
        
    import frappe


@frappe.whitelist(allow_guest=False)
def create_agency_from_payload(payload=None):

    # -------------------------------
    # PAYLOAD HANDLING
    # -------------------------------
    if not payload:
        payload = frappe.form_dict

    if isinstance(payload, str):
        payload = frappe.parse_json(payload)

    frappe.logger().info(f"Agency API payload: {payload}")

    agency_data = payload.get("agency")
    items = payload.get("items", [])
    item_group = payload.get("item_group")

    if not agency_data:
        frappe.throw("Agency data missing")

    # -------------------------------
    # TERRITORY
    # -------------------------------
    territory = agency_data.get("territory")
    if territory and not frappe.db.exists("Territory", territory):
        frappe.get_doc({
            "doctype": "Territory",
            "territory_name": territory
        }).insert(ignore_permissions=True)

    # -------------------------------
    # ITEM GROUP
    # -------------------------------
    if item_group and not frappe.db.exists("Item Group", item_group):
        frappe.get_doc({
            "doctype": "Item Group",
            "item_group_name": item_group,
            "parent_item_group": "All Item Groups",
            "is_group": 0
        }).insert(ignore_permissions=True)

    # -------------------------------
    # ITEMS
    # -------------------------------
    for row in items:
        if not frappe.db.exists("Item", row["item_code"]):
            frappe.get_doc({
                "doctype": "Item",
                "item_code": row["item_code"],
                "item_name": row["item_name"],
                "item_group": item_group,
                "stock_uom": row.get("stock_uom", "Nos"),
                "is_stock_item": 1
            }).insert(ignore_permissions=True)

    # -------------------------------
    # CONTACT
    # -------------------------------
    contact_name = None
    email = agency_data.get("primary_contact_email")

    if email:
        contact_name = frappe.db.get_value("Contact", {"email_id": email}, "name")

        if not contact_name:
            contact = frappe.get_doc({
                "doctype": "Contact",
                "first_name": agency_data.get("primary_contact_name"),
                "email_id": email,
                "mobile_no": agency_data.get("primary_contact_mobile")
            })
            contact.insert(ignore_permissions=True)
            contact_name = contact.name

    # -------------------------------
    # AGENCY
    # -------------------------------
    if frappe.db.exists("Agency", agency_data["agency_name"]):
        frappe.throw("Agency already exists")

    agency = frappe.get_doc({
        "doctype": "Agency",
        "agency_name": agency_data["agency_name"],
        "territory": territory,
        "primary_contact": contact_name,
        "is_active": agency_data.get("is_active", 1)
    })

    for row in items:
        agency.append("items", {
            "item_code": row["item_code"],
            "min_order_qty": row["min_order_qty"],
            "lead_time_days": row["lead_time_days"]
        })

    agency.insert(ignore_permissions=True)

    # -------------------------------
    # LINK CONTACT → AGENCY
    # -------------------------------
    if contact_name:
        contact = frappe.get_doc("Contact", contact_name)
        contact.append("links", {
            "link_doctype": "Agency",
            "link_name": agency.name
        })
        contact.save(ignore_permissions=True)

    # -------------------------------
    # COMMIT (CRITICAL)
    # -------------------------------
    frappe.db.commit()

    return {
        "status": "success",
        "agency": agency.name
    }

