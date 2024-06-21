import frappe
from ..api_utils.response import api_response
from datetime import datetime
#!Paginated Get Customer Details API
@frappe.whitelist(allow_guest=False,methods=["GET"])
def getAllDeliveryNote(timestamp="",limit=50,offset=0):
    #!STANDARD VALIDATION================================================================>
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

    
    delivery_note_list= frappe.get_all("Delivery Note",
        fields=["title as title",
                "is_return",
                "name as id",
                "customer",
                "customer_name",
                "posting_date",
                "address_display as billing_address",
                "shipping_address",
                "pick_list",
                "modified as updated_at",],
            
            filters={
                'modified':['>',timestamp],
                "is_return":0
            },
            limit=limit,
            order_by='-modified'
        )
    #!2 add customer_details
    for delivery_note in delivery_note_list:

        #!==========================================
        customer=delivery_note["customer"]
        customer_details=frappe.db.get_all("Customer",filters={
            "name":customer},
        fields=["territory"]
        )
        if len(customer_details)!=0:
            customer_location=customer_details[0]["territory"]
        else:
            customer_location=""
        delivery_note["customer_location"]=customer_location
        #!==========================================
        #!add child table items 
        delivery_note_id=delivery_note["id"]
        delivery_note_child_table=frappe.db.get_all("Delivery Note Item",filters={
            "parent": delivery_note_id},
        fields=["item_code","item_name","description",
                "uom","qty","serial_no","serial_and_batch_bundle","batch_no","against_sales_invoice"
                ]
        )
        #!===========================
        #! Adding Item Child Table  and batch details
   
        for delivery_note_items in delivery_note_child_table:
            batch_id=delivery_note_items["batch_no"]
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

                    delivery_note_items["qty_to_produce"]=qty_to_produce
                    delivery_note_items["produced_qty"]=produced_qty
                    delivery_note_items["expiry_date"]=expiry_date
                    delivery_note_items["manufacturing_date"]=manufacturing_date
                else:
                    delivery_note_items["qty_to_produce"]=0
                    delivery_note_items["produced_qty"]=0
                    delivery_note_items["expiry_date"]=None
                    delivery_note_items["manufacturing_date"]=None

            else:
                delivery_note_items["qty_to_produce"]=0
                delivery_note_items["produced_qty"]=0
                delivery_note_items["expiry_date"]=None
                delivery_note_items["manufacturing_date"]=None
        delivery_note["item"]=delivery_note_child_table

        #!Adding item stock

        
    
      
        
        #!adding sales invoice date and id
        if len(delivery_note_child_table)!=0:
            sales_invoice=delivery_note_child_table[0].get("against_sales_invoice")
            sales_invoice_details=frappe.db.get_all("Sales Invoice",filters={
                "name":sales_invoice},
            fields=["posting_date"]
            )
            if len(sales_invoice_details) > 0:
                delivery_note["sales_invoice"]=sales_invoice[0]
                delivery_note["sales_invoice_date"]=sales_invoice_details[0]["posting_date"]
            else:
                delivery_note["sales_invoice"]=""
                delivery_note["sales_invoice_date"]=""


    if len(delivery_note_list)==0:
        return api_response(status=True, data=[], message="Empty Content", status_code=204)
    else:
        return api_response(status=True, data=delivery_note_list, message="Successfully Fetched Delivery Note", status_code=200)
    
        
                        
   

#!================================================================

@frappe.whitelist(allow_guest=False,methods=["GET"])
def getAllSalesReturn(timestamp="",limit=50,offset=0):

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

    
    delivery_note_list= frappe.get_all("Delivery Note",
        fields=["title as title",
                "is_return",
                "name as id",
                "customer",
                "customer_name",
                "posting_date",
                "address_display as billing_address",
                "shipping_address",
                "pick_list",
                "modified as updated_at",],
            
            filters={
                'modified':['>',timestamp],
                "is_return":1
            },
            limit=limit,
            order_by='-modified'
        )
    #!add customer_details
    for delivery_note in delivery_note_list:

        #!==========================================
        customer=delivery_note["customer"]
        customer_details=frappe.db.get_all("Customer",filters={
            "name":customer},
        fields=["territory"]
        )
        if len(customer_details)!=0:
            customer_location=customer_details[0]["territory"]
        else:
            customer_location=""
        delivery_note["customer_location"]=customer_location
        #!==========================================
        #!add child table items 
        delivery_note_id=delivery_note["id"]
        
        delivery_note_child_table=frappe.db.get_all("Delivery Note Item",filters={
            "parent": delivery_note_id},
        fields=["item_code","item_name","description",
                "uom","qty","serial_no","serial_and_batch_bundle","batch_no","against_sales_invoice"
                ]
        )
        for delivery_note_items in delivery_note_child_table:
            batch_id=delivery_note_items["batch_no"]
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

                    delivery_note_items["qty_to_produce"]=qty_to_produce
                    delivery_note_items["produced_qty"]=produced_qty
                    delivery_note_items["expiry_date"]=expiry_date
                    delivery_note_items["manufacturing_date"]=manufacturing_date
                else:
                    delivery_note_items["qty_to_produce"]=0
                    delivery_note_items["produced_qty"]=0
                    delivery_note_items["expiry_date"]=None
                    delivery_note_items["manufacturing_date"]=None
            else:
                delivery_note_items["qty_to_produce"]=0
                delivery_note_items["produced_qty"]=0
                delivery_note_items["expiry_date"]=None
                delivery_note_items["manufacturing_date"]=None
        delivery_note["item"]=delivery_note_child_table
        #!adding pick list 

        
    
      
        
        #!adding sales invoice date and id
        if len(delivery_note_child_table)!=0:
            sales_invoice=delivery_note_child_table[0].get("against_sales_invoice")
            sales_invoice_details=frappe.db.get_all("Sales Invoice",filters={
                "name":sales_invoice},
            fields=["posting_date"]
            )
            if len(sales_invoice_details) > 0:
                delivery_note["sales_invoice"]=sales_invoice[0]
                delivery_note["sales_invoice_date"]=sales_invoice_details[0]["posting_date"]
            else:
                delivery_note["sales_invoice"]=""
                delivery_note["sales_invoice_date"]=""


    if len(delivery_note_list)==0:
        return api_response(status=True, data=[], message="Empty Content", status_code=204)
    else:
        return api_response(status=True, data=delivery_note_list, message="None", status_code=200)
    
        
                        
   

#!==============================================================>

@frappe.whitelist(allow_guest=False,methods=["POST"])
def create_delivery_note_confirmation(
                        delivery_note="",
                        dispatch_order_date="",
                        dispatch_order_number="",
                        customer_code="",
                        item_code="",
                        batch_no="",
                        org_code="",
                        bin_code="",
                        dispatch_qty="",
                        process_flag="",
                        error_desc="",
                        sub_inventory=""
                      ):
            
            
            if delivery_note=="":
                return api_response(status=True, data=[], message="Enter Delivery Note", status_code=400)
            if dispatch_order_number=="":
                return api_response(status=True, data=[], message="Enter Dispatch Order Number", status_code=400)
            if customer_code=="":
                return api_response(status=True, data=[], message="Enter Item Code", status_code=400)
            if sub_inventory=="":
                return api_response(status=True, data=[], message="Enter Sub Inventory", status_code=400)
            if org_code=="":
                return api_response(status=True, data=[], message="Enter Organization Code", status_code=400)
            if bin_code=="":
                return api_response(status=True, data=[], message="Enter Bin No", status_code=400)
            if batch_no=="":
                return api_response(status=True, data=[], message="Enter Batch No", status_code=400)
            if dispatch_qty=="":
                return api_response(status=True, data=[], message="Enter Qty", status_code=400)
            if process_flag=="":
                return api_response(status=True, data=[], message="Enter Process Flag", status_code=400)
            if dispatch_order_date=="":
                return api_response(status=True, data=[], message="Enter Rec Entry Date", status_code=400)
            try:
                dispatch_qty = int(dispatch_qty)
            except:
                return api_response(status=False, data=[], message="Please Enter Proper DispatchQty", status_code=400)
            try:
                dispatch_order_date = datetime.strptime(dispatch_order_date, '%Y-%m-%d')
            except:
                return api_response(status=False, data=[], message="Please Enter Proper Dispatch Order Date", status_code=400)
            #!================================================================================================================>
            if not frappe.db.exists("Delivery Note",delivery_note):
                return api_response(status=False, data=[], message="Delivery Note Does Not Exist", status_code=400)
            if not frappe.db.exists("Customer",customer_code):
                return api_response(status=False, data=[], message="Customer Does Not Exist", status_code=400)
            if not frappe.db.exists("Item",item_code):
                return api_response(status=False, data=[], message="Item Does Not Exist", status_code=400)
            #!================================================================================================================>
            try:
       
                doc = frappe.get_doc({
                            "doctype": "confirm Delivery Note Item Wise Batch Wise",
                            "delivery_note": delivery_note,
                            "dispatch_order_date": dispatch_order_date,
                            "dispatch_order_number": dispatch_order_number,
                            "customer_code": customer_code,
                            "item_code": item_code,
                            "batch_no": batch_no,
                            "org_code": org_code,
                            "bin_code": bin_code,
                            "subinventory": sub_inventory,
                            "dispatch_qty": dispatch_qty,
                            "process_flag": process_flag,
                            "error_desc": error_desc
                        })
                doc.insert()
                frappe.db.commit()
                return api_response(status=True,data=doc,message="Successfully Created Document",status_code=200)
            except Exception as e:
                    frappe.db.rollback()
                    return api_response(status=False,data='',message="Operation Failed",status_code=500)

            
            
            
            
            
            

    
        