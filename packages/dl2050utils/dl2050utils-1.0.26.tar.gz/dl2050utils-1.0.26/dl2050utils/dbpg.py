import asyncpg
import datetime
import json
from dl2050utils.core import *

# https://www.psycopg.org
# https://magicstack.github.io/asyncpg/current/index.html


TBLS_EXCLUDE = ['refs', 'trans', 'enums', 'information_schema_catalog_name', 'check_constraint_routine_usage', 'applicable_roles',
                'administrable_role_authorizations','collation_character_set_applicability', 'attributes', 'check_constraints',
                'character_sets', 'collations', 'column_domain_usage', 'column_column_usage', 'column_privileges',
                'column_udt_usage', 'columns', 'constraint_column_usage', 'schemata', 'constraint_table_usage',
                'domain_constraints', 'sql_packages', 'domain_udt_usage', 'sequences', 'domains', 'enabled_roles',
                'key_column_usage', 'parameters', 'referential_constraints', 'sql_features', 'role_column_grants',
                'routine_privileges', 'role_routine_grants', 'routines', 'sql_implementation_info', 'sql_parts',
                'sql_languages', 'sql_sizing', 'sql_sizing_profiles', 'table_constraints', 'table_privileges',
                'role_table_grants', 'views', 'tables', 'transforms', 'triggered_update_columns', '_pg_foreign_servers',
                'triggers', 'data_type_privileges', 'udt_privileges', 'role_udt_grants', 'usage_privileges', 'element_types',
                'role_usage_grants', 'user_defined_types', '_pg_foreign_table_columns', 'view_column_usage', 'view_routine_usage',
                'view_table_usage', 'foreign_server_options', 'column_options', '_pg_foreign_data_wrappers',
                'foreign_data_wrapper_options', 'foreign_tables', 'foreign_data_wrappers', 'foreign_servers',
                'foreign_table_options', 'user_mappings', 'user_mapping_options']

DRILLS = {
    'tbls': {'canal': ['zona', 'subzona', 'agente']}
}

TYPES = {
    'character varying': 'S',
    'character': 'S',
    'integer': 'I',
    'real': 'P',
    'double precision': 'F',
    'money': 'C',
    'date': 'D',
    'timestamp with time zone': 'T',
    'boolean': 'B',
    'ARRAY': 'ARRAY',
    'json': 'JSON',
    'USER-DEFINED': 'ENUM'
}

Q_DROP = """
    DROP TABLE flds;
    DROP TABLE enums;
    DROP TABLE refs;
    DROP TABLE tbls;
    DROP TYPE aligns;
"""

Q_CREATE = """
    CREATE TYPE aligns AS ENUM ('Left', 'Center', 'Right');
    
    CREATE TABLE tbls (
        tbl varchar(64) primary key,
        name varchar(64),
        keys TEXT [],
        descf varchar(64),
        drills json
    );

    CREATE TABLE flds (
        tbl varchar(64) NOT NULL references tbls(tbl),
        fld varchar(64) NOT NULL,
        name varchar(64),
        type varchar(64),
        size char(16),
        frmt char(16),
        ronly boolean,
        align aligns,
        PRIMARY KEY(tbl, fld)
    );
    
    CREATE TABLE refs (
        tbl varchar(64) NOT NULL references tbls(tbl),
        fld varchar(64) NOT NULL,
        tbl_ref varchar(64) NOT NULL references tbls(tbl),
        fld_ref varchar(64) NOT NULL
    );
    
    CREATE TABLE enums (
        name varchar(64) NOT NULL,
        values TEXT []
    );
    
"""

Q_TBLS = """
    SELECT table_name FROM information_schema.tables;
"""

Q_FLDS_ = f"""
    SELECT table_name as tbl, column_name as fld, column_name as name, data_type as type, character_maximum_length as size
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE table_name IN 
"""

Q_KEYS = """
    SELECT tc.table_name as tbl, c.column_name as fld
    FROM information_schema.table_constraints tc 
    JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name) 
    JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema
        AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
    WHERE constraint_type = 'PRIMARY KEY';
"""

Q_REFS = """
    SELECT
        tc.table_name as tbl, 
        kcu.column_name as fld, 
        ccu.table_name AS tbl_ref,
        ccu.column_name AS fld_ref
    FROM 
        information_schema.table_constraints AS tc 
        JOIN information_schema.key_column_usage AS kcu
          ON tc.constraint_name = kcu.constraint_name
          AND tc.table_schema = kcu.table_schema
        JOIN information_schema.constraint_column_usage AS ccu
          ON ccu.constraint_name = tc.constraint_name
          AND ccu.table_schema = tc.table_schema
    WHERE tc.constraint_type = 'FOREIGN KEY' and tc.constraint_name ='flds_tbl_fkey';
"""

Q_ENUMS = """
    select t.typname as ename,  
           e.enumlabel as evalue
    from pg_type t 
       join pg_enum e on t.oid = e.enumtypid  
       join pg_catalog.pg_namespace n ON n.oid = t.typnamespace;
"""

async def build_meta(db):
    for q in Q_DROP.split(";"): await db.query(q)
    for q in Q_CREATE.split(";"): await db.query(q)
    
    tbls = await db.query(Q_TBLS)
    tbls_list = [e['table_name'] for e in tbls
            if e['table_name'] not in TBLS_EXCLUDE and not e['table_name'].startswith('pg') and not e['table_name'].startswith('_pg')]
    keys = await db.query(Q_KEYS)
    tbls = [{'tbl': e, 'name': e, 'keys': [e1['fld'] for e1 in keys if e1['tbl']==e], 'drills': DRILLS[e] if e in DRILLS else {}}
            for e in tbls_list]
    await db.insert_rows('tbls', tbls, delete=False)
    
    TBLS_LIST = ', '.join([f'\'{e}\'' for e in tbls_list])
    Q_FLDS = f'{Q_FLDS_} ({TBLS_LIST});'
    flds = await db.query(Q_FLDS)
    for fld in flds:
        fld['name'] = fld['name'].title()
        fld['type'] = TYPES[fld['type']]
        fld['align'] = 'Left' if fld['type'] in ['S', 'D', 'T'] else 'Right'
    await db.insert_rows('flds', flds, delete=True)
        
    enums = await db.query(Q_ENUMS)
    enums = [{'name': e, 'values': [e1['evalue'] for e1 in enums if e1['ename']==e]} for e in set([e['ename'] for e in enums])]
    await db.insert_rows('enums', enums, delete=True)
    
    refs = await db.query(Q_REFS)
    await db.insert_rows('refs', refs, delete=True)


async def update_meta(db, meta):
    for tbl in meta['tables']:
        if 'fields' not in meta['tables'][tbl]: continue
        for fld in meta['tables'][tbl]['fields']:
            d = {'tbl': tbl, 'fld': fld}
            for attr in meta['tables'][tbl]['fields'][fld]:
                d[attr] = meta['tables'][tbl]['fields'][fld][attr]
            res = await db.update('flds', ['tbl', 'fld'], d)


async def get_meta(db):
    tbls = await db.select('tbls')
    if tbls is None: return None
    flds = await db.select('flds')
    if flds is None: return None
    meta = {'tables': {e['tbl']: {'table': e, 'fields': {e1['fld']: e1 for e1 in flds if e1['tbl']==e['tbl']}} for e in tbls}}
    return meta


def fix_types(d):
    for k in d.keys():
        if isinstance(d[k], str): d[k] = d[k].strip()
        if isinstance(d[k], datetime.date):
            d[k] = d[k].strftime("%Y-%m-%d %H:%M:%S") if isinstance(d[k], datetime.datetime) else d[k].strftime("%Y-%m-%d")
    return d

def strip(e):
    if type(e) != str: return e
    e = e.replace('\'', '')
    e.replace('\"', '')
    e.replace('\n', ' ')
    return e

def get_repr(e):
    if type(e)==list:
        items = [f'"{str(e1)}"' for e1 in e]
        return f"'{{{' ,'.join(items)}}}'"
    if type(e)==dict: return f"'{json.dumps(e)}'"
    return f"'{strip(e)}'"


class DB():
    def __init__(self, cfg, log):
        self.cfg, self.LOG = cfg, log
        try:
            passwd = self.cfg["db"]["passwd"]
        except Exception as e:
            passwd = 'rootroot'
        self.url = f'postgres://postgres:{passwd}@db:5432/postgres'

    async def startup(self, min_size=5, max_size=20):
        try:
            self.pool = await asyncpg.create_pool(self.url, min_size=min_size, max_size=max_size)
        except Exception as e:
            self.LOG.log(4, 0, label='DBPG', label2='startup', msg=str(e))
            return True
        self.LOG.log(2, 0, label='DBPG', label2='startup', msg='CONNECTED (POOL)')
        return False
    
    async def build_meta(self): return await build_meta(self)
    async def update_meta(self, meta): return await update_meta(self, meta)
    async def get_meta(self): return await get_meta(self)

    def shutdown(self):
        self.pool.terminate()  # self.pool.close()
        self.LOG.log(2, 0, label='DBPG', label2='shutdown', msg='DISCONNECTED')
        return False
    
    async def execute(self, q):
        con = await self.pool.acquire()
        try:
            res = await con.execute(q)
        except Exception as e:
            self.LOG.log(4, 0, label='DBPG', label2='execute', msg={'error_msg': str(e), 'query': q})
            return None
        finally:
            await self.pool.release(con)
        # self.LOG.log(1, 0, label='DBPG', label2='DEBUG', msg=q)
        return res
        
    async def query(self, q, one=False):
        con = await self.pool.acquire()
        try:
            if(one):
                res = await con.fetchrow(q)
                if res is None: return None
            else:
                res = await con.fetch(q)
        except Exception as e:
            self.LOG.log(4, 0, label='DB', label2='query', msg=str(e))
            return None
        finally:
            await self.pool.release(con)
        if(one): return fix_types(dict(res))
        # self.LOG.log(1, 0, label='DBPG', label2='DEBUG', msg=q)
        return [fix_types(dict(row)) for row in res]
    
    async def get_trows(self, tbl):
        q = f"SELECT COUNT(*) FROM {tbl};"
        con = await self.pool.acquire()
        try:
            res = await con.fetchrow(q)
            return dict(res)['count']
        except Exception as e:
            self.LOG.log(4, 0, label='DB', label2='get_trows', msg=str(e))
            return 0

    async def select(self, tbl, d=None, cols='*', order=None, ascending=True, offset=None, limit=None, one=False):
        if cols!='*': cols = ', '.join(cols)
        q = f"SELECT {cols}, count(*) OVER() AS nrows FROM {tbl}"
        if d is not None and len(d):
            filters = ' AND '.join([f"{k}='{d[k]}'" for k in d if d[k] is not None])
            q += f" WHERE {filters}"            
        if order is not None: q += f" ORDER BY {order} " + ("ASC" if ascending else "DESC")
        if offset is not None: q += f" OFFSET {offset}"
        if limit is not None: q += f" LIMIT {limit}"
        q += ';'
        # self.LOG.log(1, 0, label='DBPG', label2='select', msg=q)
        return await self.query(q, one=one)

    async def select_one(self, tbl, d): return await self.select(tbl, d=d, one=True)
    
    async def insert(self, tbl, d, return_key=None):
        q = f"INSERT INTO {tbl} ("
        for k in d.keys(): q += f"{k}, "
        q = q[:-2] + ") VALUES ("
        for k in d.keys(): q = q + get_repr(d[k]) + ', '
        q = q[:-2] + ")"
        # self.LOG.log(1, 0, label='DBPG', label2='insert',  msg=q)
        if return_key is not None:
            q += f" returning {return_key};"
            res = await self.query(q)
            if res is not None and len(res): return res[0][return_key]
            return None
        return await self.execute(q)
    
    async def insert_rows(self, tbl, rows, delete=False):
        if delete:
            res = await self.execute(f'DELETE FROM {tbl}')
            if res is None: return res
        for row in rows:
            res = await self.insert(tbl, row)
            if res is None: return res
        return len(rows)

    async def update(self, tbl, ks, d):
        ks = listify(ks)
        for k in ks:
            if not k in d:
                self.LOG.log(4, 0, label='DBPG', label2='update', msg=f'key error: {k}')
                return None
        setvars = ', '.join([f"{k}={get_repr(d[k])}" for k in d if k not in ks+['nrows'] and d[k] is not None])
        q = f"UPDATE {tbl} SET {setvars}"
        filters = ' AND '.join([f"{k}='{d[k]}'" for k in ks if d[k] is not None])
        q += f" WHERE {filters};"
        # self.LOG.log(1, 0, label='DBPG', label2='update',  msg=q)
        res = await self.execute(q)
        if res is None: return None
        return int(res[7:])

    async def delete(self, tbl, k, v):
        q = f"DELETE FROM {tbl}"
        if k is not None and v is not None:
            q += f" WHERE {k}='{v}'"
        q += ';'
        return await self.execute(q)
    
    async def headers(self, tbl, k, v):
        pass


if __name__ == "__main__":
    print(L([1,2,3]))