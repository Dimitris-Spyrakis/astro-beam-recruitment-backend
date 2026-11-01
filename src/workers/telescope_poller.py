import asyncio
from datetime import datetime
from typing import Annotated

import psycopg
from fastapi import APIRouter, Depends, FastAPI

router = APIRouter()
app = FastAPI()


# ------psycopg connections-----------
def get_connection():
    with psycopg.connect(
        "postgresql://postgres:beam_astro200@db.wfibpiediqlhcqizqhps.supabase.co:5432/postgres"
    ) as conn:
        yield conn


Conn = Annotated[psycopg.Connection, Depends(get_connection)]


# ---------Processing----------
def poll_oldest_obs_id(conn: Conn) -> int:
    query = (
        "SELECT id FROM observations "
        "WHERE status = 'PENDING' OR status ='PROCESSING' "
        "ORDER BY created_at ASC LIMIT 1"
    )
    with conn.cursor() as cur:
        obs_pending_id = cur.execute(query).fetchone()
        if obs_pending_id is None:
            return None
        else:
            cur.execute(
                "UPDATE observations "
                "SET status = 'PROCESSING', started_at = %(t)s "
                "WHERE id = %(obs_id)s",
                {
                    "t": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "obs_id": obs_pending_id[0],
                },
            )
            conn.commit()
            return obs_pending_id[0]


# ---------Completed----------
def polling_oldest_obs_comp(conn: Conn, id: int):
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE observations "
            "SET status = 'COMPLETED', completed_at = %(t)s, fits_file_url = %(uri)s "
            "WHERE id = %(obs_id)s",
            {
                "t": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "obs_id": id,
                "uri": "s3://astro-data/obs_<" + str(id) + ">.fits",
            },
        )
        conn.commit()


# ------------------Polling---------------
@app.get("/")
async def main(conn: Conn):
    while True:
        obs_id = poll_oldest_obs_id(conn)

        # simulating data processing
        await asyncio.sleep(3)

        polling_oldest_obs_comp(conn, obs_id)

        # poll cycle repetition
        await asyncio.sleep(5)
