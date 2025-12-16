frappe.query_reports["Agency Lead Times"] = {
    filters: [
        {
            fieldname: "agency",
            label: "Agency",
            fieldtype: "Link",
            options: "Agency",
            reqd: 1,
            on_change: function () {
                frappe.query_report.set_filter_value("item", null);
            }
        },
        {
            fieldname: "item",
            label: "Item",
            fieldtype: "Link",
            options: "Item",
            get_query: function () {
                const agency = frappe.query_report.get_filter_value("agency");

                if (!agency) {
                    return {
                        filters: {
                            name: ["=", ""]
                        }
                    };
                }

                return {
                    query: "agency_management.agency_management.report.agency_lead_times.agency_lead_times.get_items_for_agency",
                    filters: {
                        agency: agency
                    }
                };
            }
        }
    ]
};
