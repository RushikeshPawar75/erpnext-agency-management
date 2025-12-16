frappe.listview_settings["Agency"] = {
    add_fields: ["is_active"],

    get_indicator(doc) {
        if (doc.is_active === 0) {
            return ["Inactive", "red", "is_active,=,0"];
        }
        return ["Active", "green", "is_active,=,1"];
    }
};
