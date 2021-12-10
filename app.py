from logging import error
import streamlit as st
from queries.queries import apply_to_job, delete_job, show_selections, verify_user, get_name, get_all_companies, get_elligible_companies, get_reg_no, is_placed, placed_where, get_all_just_companies, insert_company, delete_company, get_comp_id, insert_job, delete_job, show_selections, get_selection, get_branch, insert_student

ADMIN_PW = 'admin'


def main():
    st.title("MIT PLACEMENT PORTAL")

    menu = ['home', 'login','selections', 'about us']

    st.sidebar.image('assets\logo.jpg', 'Manipal Institute of Technology')
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == 'home':
        
        st.markdown('''
        # HOME
        We propose a solution with 6 tables namely
        + job (details about the jobs)
        + branch (all the branches in the university)
        + students (details of the students applying)
        + company (details of the companies)
        + job_branch (details on which branch is eligible for which job)
        + selection (students placed)
        

        The students login with the student portal and the admin fills in the company details, the job details of the registered companies, and the eligibility criteria. After the job is posted, the students can check the jobs for which they are eligible and apply to the same. The tables are updated automatically according to the information passed by the companies and selected students are added to the selected tables.
        ''')
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
                
                st.markdown('''
                ## Student
                ''')
                s1, s2, s3 = st.columns(3)
                with s1:
                    sreg_no = st.text_input("Registration Number")
                    spassword = st.text_input('Student Password', type='password')
                    semester = st.selectbox('Semester', [1, 2, 3, 4, 5, 6, 7, 8])
                with s2:
                    sname = st.text_input("Name")
                    sbranch_id = st.selectbox('Branch', get_branch())
                    sbacklog = st.checkbox("Student Backlog")
                with s3:
                    semail = st.text_input("Student Email")
                    scgpa = st.text_input("Student CGPA")
                    smob_number = st.text_input("Mobile Number")
                if st.button("Insert Student"):
                    if insert_student(sreg_no, sname, semail, spassword, int(sbranch_id.split(' ')[0]), float(scgpa), int(semester), sbacklog, smob_number):                   
                        st.success("Inserted Student")
                    else:
                        st.error("ERROR: Couldn't insert Student!")

                
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
        st.markdown('''
        Harsh Rathod - 190911288
        
        Kaustav Sarkar - 190911218
        
        Ayush Goyal - 190911298
        
        MANIPAL INSTITUTE OF TECHNOLOGY
        
        DEPARTMENT OF ICT''')
                

if __name__=="__main__":
    main()