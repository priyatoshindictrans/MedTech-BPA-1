import frappe
from ..api_utils.response import api_response
from datetime import datetime
#!Paginated Get Customer Details API
@frappe.whitelist(allow_guest=False,methods=["GET"])
def getAllPickList(timestamp="",limit=50,offset=0):
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

    
    pick_list_list= frappe.get_all("Pick List",
        fields=["name as name",
                "company",
                "purpose",
                "customer",
                "customer_name",
                "work_order",
                "material_request",
                "for_qty",
                "parent_warehouse",
                "modified as updated_at",],
            
            filters={
                'modified':['>',timestamp],
            },
            limit=limit,
            order_by='-modified'
        )
   
        
    #!attach picklist item
    for pick_list in pick_list_list:
        parent_id=pick_list.get("name")
        pick_list_item=frappe.db.get_all("Pick List Item",filters={"parent":parent_id},fields=["*"])
        pick_list["items"]=pick_list_item

        #!Adding item stock
    if len(pick_list_list)==0:
        return api_response(status=True, data=[], message="Empty Content", status_code=204)
    else:
        return api_response(status=True, data=pick_list_list, message="Successfully fetched Picklist List", status_code=200)
    
        
                        
   

            
            
#!Item  Wise Batch wise Pick List Confirmation

@frappe.whitelist(allow_guest=False,methods=["POST"])
def create_pick_list_confirmation(
                        pick_list="",
                        pick_list_date="",
                        customer_code="",
                        item="",
                        batch_no="",
                        org_code="",
                        bin_code="",
                        stock_qty="",
                        picked_qty="",
                        process_flag="",
                        error_desc="",
                        sub_inventory="",
                        pick_list_purpose="",
                      ):
            
            if item=="":
                return api_response(status=True, data=[], message="Enter Item Code", status_code=400)
            if pick_list=="":
                return api_response(status=True, data=[], message="Enter Delivery Note", status_code=400)
            if pick_list_date=="":
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
            if stock_qty=="":
                return api_response(status=True, data=[], message="Enter Qty", status_code=400)
            if picked_qty=="":
                return api_response(status=True, data=[], message="Enter Qty", status_code=400)
            if process_flag=="":
                return api_response(status=True, data=[], message="Enter Process Flag", status_code=400)
            try:
                stock_qty = int(stock_qty)
                picked_qty=int(picked_qty)
            except:
                return api_response(status=False, data=[], message="Please Enter Proper Qty", status_code=400)
            try:
                pick_list_date = datetime.strptime(pick_list_date, '%Y-%m-%d')
            except:
                return api_response(status=False, data=[], message="Please Enter Proper Dispatch Order Date", status_code=400)
            #!================================================================================================================>
            if not frappe.db.exists("Pick List",pick_list):
                return api_response(status=False, data=[], message="Pick List Does Not Exist", status_code=400)
            if not frappe.db.exists("Customer",customer_code):
                return api_response(status=False, data=[], message="Customer Does Not Exist", status_code=400)
            if not frappe.db.exists("Item",item):
                return api_response(status=False, data=[], message="Item Does Not Exist", status_code=400)
            #!================================================================================================================>
            try:
       
                doc = frappe.get_doc({
                            "doctype": "Pick List Item Wise Batch Wise Confirmation",
                            "pick_list": pick_list,
                            "pick_list_date": pick_list_date,
                            "customer_code": customer_code,
                            "item": item,
                            "batch_no": batch_no,
                            "org_code": org_code,
                            "bin_code": bin_code,
                            "sub_inventory": sub_inventory,
                            "stock_qty": stock_qty,
                            "picked_qty":picked_qty,
                            "process_flag": process_flag,
                            "error_desc": error_desc,
                            "picked_list_purpose":pick_list_purpose
                        })
                doc.insert()
                frappe.db.commit()
                return api_response(status=True,data=doc,message="Successfully Created Document",status_code=200)
            except Exception as e:
                    frappe.db.rollback()
                    return api_response(status=False,data='',message="Operation Failed",status_code=500)

            
            
            