import frappe

@frappe.whitelist()
# ! envision_pms.py.link_query.prevent_closed_project_selection
# ? Function prevents users from selecting a Project that is marked as "Closed" in any document that has a "project" field.
def prevent_closed_project_selection(doc, method):
    #? Check if the document actually has a field named "project & doc.project has a value"
    if hasattr(doc, "project") and doc.project:
        
        #? If the document is not new, check if the project actually changed.
        if not doc.is_new() and not doc.has_value_changed("project"):
            return

        #? Fetch the status of the selected Project
        project_status = frappe.db.get_value("Project", doc.project, "status", cache=True)
        
        #? If status is Closed, throw Error Message
        if project_status == "Closed":
            frappe.throw(
                msg=f"You cannot select the Project <b>{doc.project}</b> because it is Closed.",
                title="Project Closed"
            )