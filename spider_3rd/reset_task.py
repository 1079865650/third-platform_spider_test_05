from db_utils import *

def reset_task_status():
    db_engine = get_engine()
    conn = db_engine.raw_connection()
    curs = conn.cursor()
    sql = """
    update spider.sp_plat_site_task set status = null;
    """   # 从表格table中读取全表内容
    curs.execute(sql)  # 执行该sql语句
    conn.commit()
    curs.close()
    conn.close()
