import streamlit as st
import pandas as pd
from db_function import (connect_to_db,
                         get_basic_info,
                         get_editional_table,
                         add_new_product,
                         get_supplier,
                         get_categories,
                         get_product,
                         get_product_history,
                         product_reorder,
                         get_pending_order,
                         receive_order)

st.sidebar.title("Invetory Management Dashboard")
option=st.sidebar.radio("Select Option:",['Baic Inforamation','Operational Tasks'])

st.title("Invetory and supply chain dashboard")

db=connect_to_db()
cursor=db.cursor(dictionary=True)


if option=="Baic Inforamation":

    st.header("Basic Metrics:")

    basic_info=get_basic_info(cursor=cursor)

    cols=st.columns(3)
    keys=list(basic_info.keys())

    for i in range(3):
        cols[i].metric(label=keys[i],value=basic_info[keys[i]])

    col=st.columns(3)
    for i in range(len(col)):
        col[i].metric(label=keys[i+3],value=basic_info[keys[i+3]])
    
    st.divider()

    editional_table=get_editional_table(cursor=cursor)
    for label,table in editional_table.items():
        st.header(label)
        df=pd.DataFrame(table)
        st.dataframe(df)
        st.divider()


elif option=='Operational Tasks':
    st.header("Operational Tasks")

    user_task=st.selectbox("Choose a Task",['Add New Product','Product History',
                                            'Place Reorder','Receive Order'])
    st.divider()
    if user_task=='Add New Product':
         st.header("Add New Product")

         category=get_categories(cursor)
         supplier=get_supplier(cursor)
         supplier_id=[s['supplier_id'] for s in supplier]
         supplier_name=[s['supplier_name'] for s in supplier]

         with st.form("Add New Product"):
            product_name=st.text_input("Enter name of product")
            product_category=st.selectbox("Select category of procuct",category)
            product_price=st.number_input("Enter price of product",min_value=0)
            stock_quantity=st.number_input("Enter quantity of product",min_value=0)
            reorder_level=st.number_input("Enter reorder level",min_value=0)
            supplier_id=st.selectbox("Select supplier ",options=supplier_id,
                                     format_func=lambda x:supplier_name[supplier_id.index(x)])
            if st.form_submit_button("Submit"):
                if not product_name:
                    st.error("Please enter product name")
                else:
                    try:
                        add_new_product(cursor,
                                        db,
                                        product_name,
                                        product_category,
                                        product_price,
                                        stock_quantity,
                                        reorder_level,
                                        supplier_id
                                        )
                        st.success(f"{product_name} added succesfully...")
                    except:
                        st.error("Something Error Occured.......")

    elif user_task=="Product History":
        st.header("Product History")
        products=get_product(cursor=cursor)
        product_id=[id['product_id'] for id in products]
        product_name=[name['product_name'] for name in products]

        user_input_product_id=st.selectbox("Select Product ",options=product_id,
                                     format_func=lambda x:product_name[product_id.index(x)])
        if st.button("Show history"):
            product_data=get_product_history(cursor,user_input_product_id)
            df=pd.DataFrame(product_data)
            st.dataframe(df)

    elif user_task=="Place Reorder":
        st.header("Place Reorder")
        products=get_product(cursor=cursor)
        product_id=[id['product_id'] for id in products]
        product_name=[name['product_name'] for name in products]

        user_input_product_id=st.selectbox("Select Reorder Product ",options=product_id,
                                     format_func=lambda x:product_name[product_id.index(x)])
        
        stock_quantity=st.number_input("Enter quantity of product",min_value=0)
        if st.button("Submit"):
            try:
                product_reorder(cursor,db,user_input_product_id,stock_quantity)
                st.success("Order placed succesfully")
            except:
                print("Something error occured.....")
    elif user_task=="Receive Order":
        st.header("Mark reorder as Received")
        pending_data=get_pending_order(cursor=cursor)
        if not pending_data:
            st.info("No pending order to recieve")
        else:
            reorder_id=[id['reorder_id'] for id in pending_data]
            reorder_labels=[f"ID {r['reorder_id']} - {r['product_name']}" for r in pending_data]
            
            selected_label=st.selectbox("Select reorder to mark as recevied",options=reorder_labels)

            if selected_label:
                selected_reorder_id=reorder_id[reorder_labels.index(selected_label)]

                if st.button("Mark as Recevied"):
                    try:
                        receive_order(cursor,db,selected_reorder_id)
                        st.success(f"Reorder id {selected_reorder_id} mark as recevied")
                    except:
                        st.error("Something error occured...")