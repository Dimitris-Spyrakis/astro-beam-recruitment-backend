import asyncio
from datetime import datetime
from typing import Annotated

import psycopg
from fastapi import APIRouter, BackgroundTasks, Depends, FastAPI
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr

app = FastAPI()


# -------app----------
app = FastAPI()
router = APIRouter()


# ------psycopg connections-----------
def get_connection():
    with psycopg.connect(
        "postgresql://postgres:beam_astro200@db.wfibpiediqlhcqizqhps.supabase.co:5432/postgres"
    ) as conn:
        yield conn


Conn = Annotated[psycopg.Connection, Depends(get_connection)]


# -------------Email-----------------------
class EmailSchema(BaseModel):
    email: list[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME="astro",
    MAIL_PASSWORD="pwd",
    MAIL_FROM="astro@gmail.com",
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    MAIL_FROM_NAME="Jim",
    SUPPRESS_SEND=True,
    USE_CREDENTIALS=False,
    VALIDATE_CERTS=False,
)


# --------------Sending Email-----------------
async def send_in_background(
    cond: bool, email: EmailSchema, background_tasks: BackgroundTasks
) -> str:
    if bool:
        message = MessageSchema(
            subject="Observation Complete",
            recipients=email,
            body="Simple background task",
            subtype=MessageType.plain,
        )

        fm = FastMail(conf)

        background_tasks.add_task(fm.send_message, message)

        print("Email sent")
        print(message)


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
async def polling_oldest_obs_comp(conn: Conn, id: int) -> bool:
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
        return True


# ------------------Polling---------------
@app.get("/")
async def main(conn: Conn, backTask: BackgroundTasks):
    email = ["random@gmail.com"]
    while True:
        # fetching oldest observation id
        obs_id = poll_oldest_obs_id(conn)

        # simulating data processing
        await asyncio.sleep(3)

        # marking it as completed
        cond = await polling_oldest_obs_comp(conn, obs_id)

        # check completed status to send email
        await send_in_background(cond, email, backTask)

        # poll cycle repetition
        await asyncio.sleep(5)
