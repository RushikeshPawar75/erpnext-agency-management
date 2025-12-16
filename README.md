### Agency Management

agency

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app agency_management
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/agency_management
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit


MODULE 1: AGENCY MANAGEMENT
==========================

Overview
--------
The Agency Management module manages pharmaceutical agencies that supply stock items.
It supports agency–item relationships, validations, supplier creation, REST-based onboarding,
and analytical reporting.

Target Platform: ERPNext v15+ / Frappe Framework


FEATURES
--------

1. DocTypes

Agency
- agency_name (Data, Unique)
- territory (Link → Territory)
- primary_contact (Link → Contact)
- is_active (Check)

Agency Item (Child Table)
- item_code (Link → Item)
- min_order_qty (Int)
- lead_time_days (Int)


2. Business Validations

- Prevent deactivating an Agency if Agency Items exist
- Prevent duplicate items in Agency Item table
- min_order_qty must be greater than 0
- lead_time_days cannot be negative

Implemented in Agency.validate()


3. UI Enhancements

List View Indicator
- Inactive Agencies are shown in RED
- Active Agencies are shown in GREEN

Custom Button: Create Supplier
- Visible only for saved Agency records
- Creates a Supplier using agency_name


4. REST API – Create Agency with Items

Endpoint:
POST /api/method/agency_management.api.create_agency_from_payload

Behavior:
- Creates Territory if missing
- Creates Item Group if missing
- Creates Items if missing
- Creates Contact
- Creates Agency
- Creates Agency Items
- Links Contact to Agency

Sample Payload:
{
  "agency": {
    "agency_name": "Apollo Pharma Distributors",
    "territory": "India",
    "is_active": 1
  },
  "item_group": "Drugs",
  "items": [
    {
      "item_code": "PCME-250",
      "item_name": "Paracetamol 250mg",
      "min_order_qty": 100,
      "lead_time_days": 7,
      "stock_uom": "Nos",
      "valuation_rate": 2.5
    }
  ]
}


5. Report – Agency Lead Times

Columns:
- Agency
- Item
- Minimum Order Quantity
- Lead Time (Days)

Purpose:
- Supply chain planning
- Vendor SLA tracking


FIXTURES / SAMPLE DATA
---------------------
- 2 Agencies
- 3 Items
- 1 Territory
- 1 Item Group


AI USAGE LOG (SUMMARY)
---------------------
Issue: Prevent deactivation with child rows
Prompt: How to prevent disabling DocType with child records in ERPNext?
AI Suggested: Use validate() method
Implemented: validate_active_status()

Issue: Duplicate child rows
Prompt: How to prevent duplicate rows in child table?
AI Suggested: Track seen items using a set
Implemented: validate_agency_items()
