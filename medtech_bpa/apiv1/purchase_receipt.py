import frappe
from ..api_utils.response import api_response
from datetime import datetime
#!Paginated Get Customer Details API
@frappe.whitelist(allow_guest=False,methods=["GET"])
def getAllpurchaseReceipt(timestamp="",limit=50,offset=0):

    #!STANDARD VALIDATIONS 1================================================================
    #TODO 1: limit offset int format check
    try:
        limit = int(limit)
        offset = int(offset)
    except:
        return api_response(status=False, data=[], message="Please Enter Proper Limit and Offset", status_code=400)
    #!limit and offset upper limit validation
    if limit > 200 or limit < 0 or offset<0:
        return api_response(status=False, data=[], message="Limit exceeded 500", status_code=400)
    #!timestamp non empty validation
    if timestamp is None or timestamp =="":
        return api_response(status=False, data=[], message="Please Enter a timestamp", status_code=400)
    #!timestamp format validation
    try:
        timestamp_datetime=datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        return api_response(status=False, data=[], message=f"Please Enter a valid timestamp {e}", status_code=400)
    #!=================================================================================================
    
    #!2 GETTING PURCHASE RECEIPT
    purchase_receipt_list = frappe.get_all("Purchase Receipt",
        fields=["name as id",
                "title as title",
                "is_return",
                "supplier",
                "supplier_name",
                "posting_date",
                "supplier_delivery_note",
                "modified as updated_at",
                ],
            
            filters={
                'modified':['>',timestamp],
                 "is_return":0,
            },
            limit=limit,
            order_by='-modified'
        )
    #! Adding Item Child Table  and batch details
    for purchase_receipt in purchase_receipt_list:
        purchase_receipt_id=purchase_receipt["id"]
        purchase_receipt_child_table=frappe.db.get_all("Purchase Receipt Item",filters={
            "parent": purchase_receipt_id},
        fields=["item_code","supplier_part_no","item_name","description",
                "uom","received_qty","qty","rejected_qty","serial_no",
                "serial_and_batch_bundle","rejected_serial_and_batch_bundle",
                "batch_no"
                ]
        )
        for purchase_receipt_child in purchase_receipt_child_table:
            batch_id=purchase_receipt_child["batch_no"]
            if batch_id is not None:
                batch_details=frappe.db.get_all("Batch",filters={
                    "name":batch_id
                },fields=["name","qty_to_produce","produced_qty","expiry_date","manufacturing_date"])
                if len(batch_details) > 0:
                    batch_details=batch_details[0]
                    qty_to_produce =batch_details["qty_to_produce"]
                    produced_qty=batch_details["produced_qty"]
                    expiry_date=batch_details["expiry_date"]
                    manufacturing_date=batch_details["manufacturing_date"]

                    purchase_receipt_child["qty_to_produce"]=qty_to_produce
                    purchase_receipt_child["produced_qty"]=produced_qty
                    purchase_receipt_child["expiry_date"]=expiry_date
                    purchase_receipt_child["manufacturing_date"]=manufacturing_date
                else:
                    purchase_receipt_child["qty_to_produce"]=0
                    purchase_receipt_child["produced_qty"]=0
                    purchase_receipt_child["expiry_date"]=None
                    purchase_receipt_child["manufacturing_date"]=None
            else:
                    purchase_receipt_child["qty_to_produce"]=0
                    purchase_receipt_child["produced_qty"]=0
                    purchase_receipt_child["expiry_date"]=None
                    purchase_receipt_child["manufacturing_date"]=None
        purchase_receipt["item"]=purchase_receipt_child_table

    #!============================================================
    if len(purchase_receipt_list)==0:
        return api_response(status=True, data=[], message="Empty Content", status_code=204)
    else:
        return api_response(status=True, data=purchase_receipt_list, message="None", status_code=200)
    
        
#!================================================================
#!Purchase Return
import frappe
from ..api_utils.response import api_response
from datetime import datetime
#!Paginated Get Customer Details API
@frappe.whitelist(allow_guest=False,methods=["GET"])
def getAllpurchaseReturn(timestamp="",limit=50,offset=0):

    #TODO 1: limit offset int format check
    try:
        limit = int(limit)
        offset = int(offset)
    except:
        return api_response(status=False, data=[], message="Please Enter Proper Limit and Offset", status_code=400)
    #!limit and offset upper limit validation
    if limit > 200 or limit < 0 or offset<0:
        return api_response(status=False, data=[], message="Limit exceeded 500", status_code=400)
    #!timestamp non empty validation
    if timestamp is None or timestamp =="":
        return api_response(status=False, data=[], message="Please Enter a timestamp", status_code=400)
    #!timestamp format validation
    try:
        timestamp_datetime=datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        return api_response(status=False, data=[], message=f"Please Enter a valid timestamp {e}", status_code=400)

    
    purchase_receipt_list = frappe.get_all("Purchase Receipt",
        fields=["name as id",
                "title as title",
                "is_return",
                "supplier",
                "supplier_name",
                "posting_date",
                "supplier_delivery_note",
                "modified as updated_at",
                ],
            
            filters={
                'modified':['>',timestamp],
                 "is_return":1,
            },
            limit=limit,
            order_by='-modified'
        )
    for purchase_receipt in purchase_receipt_list:
        purchase_receipt_id=purchase_receipt["id"]
        purchase_receipt_child_table=frappe.db.get_all("Purchase Receipt Item",filters={
            "parent": purchase_receipt_id},
        fields=["item_code","supplier_part_no","item_name","description",
                "uom","received_qty","qty","rejected_qty","serial_no",
                "serial_and_batch_bundle","rejected_serial_and_batch_bundle",
                "batch_no"
                ]
        )
        purchase_receipt["item"]=purchase_receipt_child_table

    #! Adding Item Child Table  and batch details
    for purchase_receipt in purchase_receipt_list:
        purchase_receipt_id=purchase_receipt["id"]
        purchase_receipt_child_table=frappe.db.get_all("Purchase Receipt Item",filters={
            "parent": purchase_receipt_id},
        fields=["item_code","supplier_part_no","item_name","description",
                "uom","received_qty","qty","rejected_qty","serial_no",
                "serial_and_batch_bundle","rejected_serial_and_batch_bundle",
                "batch_no"
                ]
        )
        for purchase_receipt_child in purchase_receipt_child_table:
            batch_id=purchase_receipt_child["batch_no"]
            if batch_id is not None:
                batch_details=frappe.db.get_all("Batch",filters={
                    "name":batch_id
                },fields=["name","qty_to_produce","produced_qty","expiry_date","manufacturing_date"])
                if len(batch_details) > 0:
                    batch_details=batch_details[0]
                    qty_to_produce =batch_details["qty_to_produce"]
                    produced_qty=batch_details["produced_qty"]
                    expiry_date=batch_details["expiry_date"]
                    manufacturing_date=batch_details["manufacturing_date"]

                    purchase_receipt_child["qty_to_produce"]=qty_to_produce
                    purchase_receipt_child["produced_qty"]=produced_qty
                    purchase_receipt_child["expiry_date"]=expiry_date
                    purchase_receipt_child["manufacturing_date"]=manufacturing_date
                else:
                    purchase_receipt_child["qty_to_produce"]=0
                    purchase_receipt_child["produced_qty"]=0
                    purchase_receipt_child["expiry_date"]=None
                    purchase_receipt_child["manufacturing_date"]=None
            else:
                    purchase_receipt_child["qty_to_produce"]=0
                    purchase_receipt_child["produced_qty"]=0
                    purchase_receipt_child["expiry_date"]=None
                    purchase_receipt_child["manufacturing_date"]=None
        purchase_receipt["item"]=purchase_receipt_child_table

                

    if len(purchase_receipt_list)==0:
        return api_response(status=True, data=[], message="Empty Content", status_code=204)
    else:
        return api_response(status=True, data=purchase_receipt_list, message="None", status_code=200)
    
        
                        
   


                        
   


@frappe.whitelist(allow_guest=False,methods=["POST"])
def create_purchase_receipt_confirmation(
                      visual_inspection_report="",
                      organization_code="",
                      po_number="",
                      item_code="",
                      sub_inventory="",
                      bin_no="",
                      batch_no="",
                      qty="",
                      process_flag="",
                      error_message="",
                      rec_entry_date=""
                      ):
            if visual_inspection_report=="":
                return api_response(status=True, data=[], message="Enter Visual Inspection Report/Purchase Receipt", status_code=400)
            if po_number=="":
                return api_response(status=True, data=[], message="Enter PO Number", status_code=400)
            if item_code=="":
                return api_response(status=True, data=[], message="Enter Item Code", status_code=400)
            if sub_inventory=="":
                return api_response(status=True, data=[], message="Enter Sub Inventory", status_code=400)
            if organization_code=="":
                return api_response(status=True, data=[], message="Enter Organization Code", status_code=400)
            if bin_no=="":
                return api_response(status=True, data=[], message="Enter Bin No", status_code=400)
            if batch_no=="":
                return api_response(status=True, data=[], message="Enter Batch No", status_code=400)
            if qty=="":
                return api_response(status=True, data=[], message="Enter Qty", status_code=400)
            if process_flag=="":
                return api_response(status=True, data=[], message="Enter Process Flag", status_code=400)
            if rec_entry_date=="":
                return api_response(status=True, data=[], message="Enter Rec Entry Date", status_code=400)
            try:
                qty = int(qty)
            except:
                return api_response(status=False, data=[], message="Please Enter Proper Qty", status_code=400)
            try:
                rec_entry_date = datetime.strptime(rec_entry_date, '%Y-%m-%d')
            except:
                return api_response(status=False, data=[], message="Please Enter Proper Rec Entry Date", status_code=400)
            if not frappe.db.exists("Purchase Receipt",visual_inspection_report):
                return api_response(status=False, data=[], message="Visual Inspection Report Does Not Exist", status_code=400)
            if not frappe.db.exists("Item",item_code):
                return api_response(status=False, data=[], message="Item Does Not Exist", status_code=400)
            
            try:
        # Create a new document for the custom doctype
                doc = frappe.get_doc({
                    "doctype": "Purchase Receipt Item Wise Batch Wise Confirmation",  # Replace with your actual doctype name
                    "visual_inspection_report": visual_inspection_report,
                    "organisation_code": organization_code,
                    "po_number": po_number,
                    "item_code": item_code,
                    "sub_inventory": sub_inventory,
                    "bin_no": bin_no,
                    "batch_no": batch_no,
                    "qty": qty,
                    "process_flag": process_flag,
                    "error_message": error_message,
                    "rec_entry_date": rec_entry_date
                })
                # Insert the document into the database
                doc.insert()
                frappe.db.commit()
                return api_response(status=True,data=doc,message="Successfully Created Document",status_code=200)
            except Exception as e:
                    frappe.db.rollback()
                    return api_response(status=False,data='',message="Operation Failed",status_code=500)

            
            
            