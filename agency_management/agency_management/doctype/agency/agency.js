frappe.ui.form.on("Agency", {
    onload: function (frm) {
        frm.set_query("item_code", "items", function () {
            return {
                filters: {
                    is_stock_item: 1,
                    item_group: "Drugs"
                }
            };
        });
    },

    refresh: function (frm) {
        if (!frm.is_new()) {
            frm.add_custom_button("Create Supplier", function () {
                frappe.call({
                    method: "agency_management.agency_management.doctype.agency.agency.create_supplier",
                    args: {
                        agency: frm.doc.name
                    },
                    callback: function (r) {
                        if (r.message) {
                            frappe.set_route("Form", "Supplier", r.message);
                        }
                    }
                });
            });
        }
    }
});
