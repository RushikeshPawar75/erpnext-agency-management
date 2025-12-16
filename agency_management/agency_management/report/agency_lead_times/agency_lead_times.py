import frappe


def execute(filters=None):
    filters = filters or {}

    conditions = ""
    values = {}

    if filters.get("agency"):
        conditions += " AND a.name = %(agency)s"
        values["agency"] = filters["agency"]

    if filters.get("item"):
        conditions += " AND ai.item_code = %(item)s"
        values["item"] = filters["item"]

    columns = [
        {"label": "Agency", "fieldname": "agency", "fieldtype": "Link", "options": "Agency"},
        {"label": "Item", "fieldname": "item", "fieldtype": "Link", "options": "Item"},
        {"label": "Min Order Qty", "fieldname": "min_order_qty", "fieldtype": "Float"},
        {"label": "Lead Time (Days)", "fieldname": "lead_time_days", "fieldtype": "Int"},
    ]

    data = frappe.db.sql(f"""
        SELECT
            a.name AS agency,
            ai.item_code AS item,
            ai.min_order_qty,
            ai.lead_time_days
        FROM
            `tabAgency` a
        JOIN
            `tabAgency Item` ai ON ai.parent = a.name
        WHERE
            a.is_active = 1
            {conditions}
    """, values, as_dict=True)

    return columns, data



@frappe.whitelist()
def get_items_for_agency(doctype, txt, searchfield, start, page_len, filters):
    agency = None

    if filters and isinstance(filters, dict):
        agency = filters.get("agency")

    if not agency:
        return []

    return frappe.db.sql(
        """
        SELECT DISTINCT
            ai.item_code AS name,
            ai.item_code
        FROM
            `tabAgency Item` ai
        WHERE
            ai.parent = %s
            AND ai.item_code LIKE %s
        LIMIT %s OFFSET %s
        """,
        (
            agency,
            f"%{txt}%",
            page_len,
            start
        )
    )
