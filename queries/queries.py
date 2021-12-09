import mysql.connector
from decouple import config
from unipath import Path
import pandas as pd

BASE_DIR = Path(__file__).parent

host = config('host', default=False, cast=str)
user = config('user', default=False, cast=str)
passwd = config('passwd', default=False, cast=str)
database = config('database', default=False, cast=str)

mydb = mysql.connector.connect(
    host=host, 
    user=user,
    passwd=passwd, 
    database=database
    )

mycursor = mydb.cursor()
# mycursor.execute("show tables")
# res = mycursor.fetchall();
# for i in res:
#     print(i[0])


def verify_user(username: str, password: str):
    '''
    Takes in input username and the password and then outputs if the user exists then returns true else false
    '''
    mycursor.execute(f"select * from student where email='{username}' and password = '{password}'")
    result = mycursor.fetchall()
    
    if(result != []):
        return True
    else: 
        return False

def show_selections(filter: str):
    mycursor.execute(f"select sel.reg_no, s.name, sel.job_id, c.name, j.title, j.role, b.name from selection sel join student s on sel.reg_no = s.reg_no join job j on j.job_id = sel.job_id join branch b on b.branch_id = s.branch_id join company c on c.comp_id = j.comp_id order by {filter}")
    result = mycursor.fetchall()
    col_names = ['reg no', 'student name', 'job id', 'company name','job title', 'role', 'branch']
    df = pd.DataFrame(columns=col_names, data=result)
    return df

def get_name(username: str):
    mycursor.execute(f"select name from student where email='{username}'")
    result = mycursor.fetchone()
    return result[0]

def get_selection(reg_no: int):
    try:
        mycursor.execute(f"with result as (select job_id from selection where reg_no = {reg_no}) select c.comp_id, c.name, j.role, j.title, j.type from result r join job j on j.job_id = r.job_id join company c on c.comp_id = j.comp_id")
        result = mycursor.fetchall()
        col_names = ['Comp Id', 'Company Name', 'Role', 'Title', 'Type']
        df = pd.DataFrame(columns=col_names, data=result)
        return df
    except Exception as e:
        print(e)
        return pd.DataFrame()
def format_column_names(names):
    names_list = []
    for i in names:
        names_list.append(i[0])
    return names_list

def get_column_names(table_name: str):
    mycursor.execute(f"SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='dbms_project' AND `TABLE_NAME`='{table_name}'")
    column_names = mycursor.fetchall()
    column_names = format_column_names(column_names)
    return column_names

def get_all_companies():
    mycursor.execute(f"select company.name, job.* from job, company where job.comp_id = company.comp_id")
    result = mycursor.fetchall()
    column_names = get_column_names('job')
    column_names.insert(0,'name')
    df = pd.DataFrame(columns = column_names, data = result)
    return df

def get_all_just_companies():
    mycursor.execute(f"select * from company")
    result = mycursor.fetchall()
    column_names = get_column_names('company')

    df = pd.DataFrame(columns = column_names, data = result)
    return df

def insert_company(id: int, name: str, phone: str):
    try:
        mycursor.execute(f"INSERT INTO company VALUES ({id}, '{name}', '{phone}')")
        mydb.commit()
        return True
    except Exception as e:
        print(e)
        return False
def delete_company(id: int):
    try:
        mycursor.execute(f"delete from company where comp_id = {id}")
        mydb.commit()
        return True
    except Exception as e:
        print(e)
        return False

def placed_where(reg_id: int):
    mycursor.execute(f"select company.name, selection.job_id, job.role from selection, company, job where selection.reg_no = {reg_id} and job.job_id = selection.job_id and job.comp_id = company.comp_id")
    result = mycursor.fetchone()
    return result

def get_comp_id():
    mycursor.execute(f"select comp_id, name from company")
    id_list = [str(i[0])+' '+i[1] for i in mycursor.fetchall()]
    return id_list

def insert_job(job_id: int, comp_id: int, title: str, role: str, ctc: int, cgpa: float, type: str, backlog: int, location: str):
    try:
        mycursor.execute(f"INSERT INTO job VALUES ({job_id}, {comp_id}, '{title}', '{role}', {ctc}, {cgpa}, '{type}', {backlog}, '{location}')")
        mydb.commit()
        return True, ''
    except Exception as e:
        print(e)
        return False, e
def delete_job(id: int):
    try:
        mycursor.execute(f"delete from job where job_id = {id}")
        mydb.commit()
        return True
    except Exception as e:
        print(e)
        return False


def get_elligible_companies(reg_id: int):
    mycursor.execute(f"select company.name, job.* from job, company, student, job_branch where student.reg_no = {reg_id} and student.backlog <= job.backlog and job.job_id = job_branch.job_id and job_branch.branch_id = student.branch_id and job.comp_id = company.comp_id and job.cgpa <= student.cgpa")
    result = mycursor.fetchall()
    column_names = get_column_names('job')
    column_names.insert(0,'name')
    df = pd.DataFrame(columns = column_names, data = result)
    return df
def is_placed(reg_no: int):
    mycursor.execute(f"select count(*) from selection where reg_no = {reg_no}")
    result = mycursor.fetchall()
    if result[0][0] == 0:
        return False
    else: 
        return True

def is_elligible(job_id: int, reg_no: int):
    df = get_elligible_companies(reg_no)
    ell_id = list(df['job_id'])
    
    if job_id in ell_id:
        return True
    else:
        return False


def apply_to_job(job_id: int, reg_no: int):
    if not is_placed(reg_no) and is_elligible(job_id, reg_no):
        try:
            mycursor.execute(f"insert into selection values({job_id}, {reg_no})")
            mydb.commit()
            return True
        except:
            print("ERROR: Can't apply to this job")
            return False
    else:
        return False
    
def get_reg_no(username: str):
    mycursor.execute(f"select reg_no from student where email='{username}'")
    result = mycursor.fetchone()
    return result[0]


if __name__=="__main__":
    print(is_elligible(1008, 190904314 ))
