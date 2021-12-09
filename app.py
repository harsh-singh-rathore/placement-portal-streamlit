import streamlit as st
from queries.queries import apply_to_job, delete_job, show_selections, verify_user, get_name, get_all_companies, get_elligible_companies, get_reg_no, is_placed, placed_where, get_all_just_companies, insert_company, delete_company, get_comp_id, insert_job, delete_job, show_selections, get_selection

ADMIN_PW = 'admin'


def main():
    st.title("MIT PLACEMENT PORTAL")

    menu = ['home', 'login','selections', 'about us']

    st.sidebar.image('assets\logo.jpg', 'Manipal Institute of Technology')
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == 'home':
        
        st.markdown('''
        <h1> HOME </h1>
        + This is the placement portal for the students of MIT and they can use this to apply for companies and see if they are shortlisted
        + The app is based on Streamlit which is a python framework and MySql for database
        ''', unsafe_allow_html=True)
    if choice == 'login':
        st.subheader('LOGIN')
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input('Password', type='password')
        if st.sidebar.checkbox("LOGIN"):
            if(username == 'admin' and password == ADMIN_PW):
                st.write(f"Hello, Admin")
                
                
                st.markdown('''
                ## COMPANIES
                ''')
                st.write(get_all_just_companies())
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    comp_id = st.text_input("Company Id")
                with col2:
                    comp_name = str(st.text_input("Company Name"))
                with col3:
                    company_contact = str(st.text_input("Company Contact"))

                b1, b2 = st.columns(2)
                with b1:
                    if st.button("insert"):
                        incomp = insert_company(int(comp_id), comp_name, company_contact)
                        if incomp:
                            st.success("Inserted company")
                        else:
                            st.error("Could Not insert company")
                with b2:
                    if st.button("delete"):
                        incomp = delete_company(int(comp_id))
                        if incomp:
                            st.success("Delete Company")
                        else:
                            st.error("Could Not delete company")


                st.markdown('''
                ## JOBS
                ''')
                st.write(get_all_companies())
                j1, j2, j3 = st.columns(3)


                with j1:
                    jobv_id = st.text_input("Job Id")
                    job_ctc= st.text_input("CTC") 
                    job_loc = st.text_input("Location",max_chars = 256)
                with j2:
                    job_comp_id = st.selectbox("Comp Id", get_comp_id())
                    job_cgpa = str(st.text_input("CGPA"))
                    job_type = st.selectbox("Type", ['PI', 'P', 'I', 'SI'])
                with j3:
                    job_title = str(st.text_input("Title",max_chars = 256))
                    job_role = str(st.text_input("Role",max_chars = 256))
                    job_backlog = st.checkbox("Backlog")
                if job_backlog:
                    job_backlog_int = 1
                else:
                    job_backlog_int = 0
                d1, d2 = st.columns(2)
                with d1:
                    if st.button("Insert Job"):
                        ret, err = insert_job(jobv_id, int(job_comp_id.split(' ')[0]), job_title, job_role, job_ctc, job_cgpa, job_type, job_backlog_int, job_loc)
                        if ret:
                            st.success("Inserted Job")
                        else:
                            st.error(err)
                with d2:
                    if st.button("Delete Job"):
                        ret = delete_job(jobv_id)
                        if ret:
                            st.success("Deleted Job")
                        else:
                            st.error("Error Deleting Job")



                
            elif(not verify_user(username, password)):
                st.error('incorrect password or username')
            else:
                st.write(f"Hello, {get_name(username=username)}")
                reg_no = get_reg_no(username)

                option = 'All Companies'
                option = st.selectbox(
                    'Filter',
                    ('All Companies', 'Elligible'))
                if option == 'All Companies':
                    st.write(get_all_companies())
                elif option == 'Elligible':
                    st.write(get_elligible_companies(reg_no))
                job_id = st.text_input('Apply to job_id')
                if st.button('APPLY'):
                    if is_placed(reg_no):
                        where = placed_where(reg_no)
                        st.error(f"Cannot sit for further placements already placed at {where[0]} as an {where[2]} ")
                    else:
                        if apply_to_job(int(job_id), reg_no):
                            st.success("Placed!")
                        else:
                            st.error("Could not apply")

    if choice == 'selections':
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input('Password', type='password')
        if st.sidebar.checkbox("LOGIN"):
            if(username == 'admin' and password == ADMIN_PW):
                st.write(f"Hello, Admin")
                filter = ['Student Name', 'Company Name', 'Branch', 'Role']
                option = st.selectbox('Filter', filter)
                filt = 's.name'
                if option == 'Company Name':
                    filt = 'c.name'
                elif option == 'Branch':
                    filt = 'b.name'
                elif option == 'Role':
                    filt = 'j.role'
                st.write(show_selections(filt))
            elif(not verify_user(username, password)):
                st.error('incorrect password or username')
            else:
                st.write(f"Hello, {get_name(username=username)}")
                reg_no = get_reg_no(username)
                st.write(get_selection(reg_no))

    if choice == 'about us':
        st.subheader('About Us')
                

if __name__=="__main__":
    main()