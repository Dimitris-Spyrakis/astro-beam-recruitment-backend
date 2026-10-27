from fastapi import FastAPI, HTTPException, Request, status,Depends
from schemas import Observations
from pydantic import Strict
#favicon error
from typing import List,Dict,Annotated

import psycopg

import xml.etree.ElementTree as ET
from psycopg.adapt import Dumper
 

#------psycopg connections-----------
def get_connection():
        with psycopg.connect("postgresql://postgres:beam_astro200@db.wfibpiediqlhcqizqhps.supabase.co:5432/postgres") as conn:
             yield conn

Conn = Annotated[psycopg.Connection, Depends(get_connection)]


app = FastAPI()

#------------HTTP-Restpoints-------------------- 

#-----------Restpoints-------------------------

@app.get("/")
def root(conn: Conn) -> str:
    return "Hello ASTRO!"

#(get)/observations/
@app.get("/observations")
def list_observations(conn: Conn) -> tuple:

    query = "SELECT id,center_freq_mhz,status,created_at FROM observations ORDER BY status = 'PENDING' DESC, created_at ASC;"
    with conn.cursor() as cur:
        result=cur.execute(query).fetchall()
    return result

#(get)/observations/{id}
@app.get("/observations/{id}")
def fetch_observations_id(conn: Conn, id: int) -> tuple:
    with conn.cursor() as cur1:
        result = cur1.execute("SELECT id,center_freq_mhz,status,created_at FROM observations WHERE id = %(id)s",{'id':id}).fetchone()
        if result==None:
            raise HTTPException(status_code=404,detail="No such id: " + str(id))   
    return result
    
        
#(post)/observations/
@app.post("/obserations")
def create_observation(conn: Conn, center_freq_mhz: float) -> str:
    if center_freq_mhz<1400.0 or center_freq_mhz>1440.0:
        raise HTTPException(status_code=404,detail="out of range frequency: "+ str(center_freq_mhz)+" (freq[1400.0,1440.0])")
    else:
        with conn.cursor() as cur:
            new_observation_id = cur.execute("SELECT MAX(id) FROM observations").fetchone()
            res = int(new_observation_id[0]+1)
            result = cur.execute("INSERT INTO observations (id,center_freq_mhz, status) VALUES (%(new_observation_id)s,%(center_freq_mhz)s, 'PENDING')",
            {'center_freq_mhz':center_freq_mhz,'new_observation_id':res})
        return "Observation saved"
