from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import psycopg2

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

conn = psycopg2.connect(
    host='postgres',
    port='5432',
    dbname='default_db',
    user='default',
    password='secret123'
)


@app.get("/")
async def get_index():
    # Serve the index.html file
    return FileResponse("static/index.html")


@app.get("/api/flats")
def get_tuples():
    # Collect all items from the database...
    with conn.cursor() as cursor:
        select_query = "SELECT title, image_url FROM flats_sell"
        cursor.execute(select_query)
        tuples = cursor.fetchall()

    # ... and return them to the user.
    result = []
    for tuple_item in tuples:
        result.append({"title": tuple_item[0], "image_url": tuple_item[1]})

    # 'size' for debugging purposes.
    return {'size': len(result), 'result': result}


@app.on_event("shutdown")
def shutdown_event():
    conn.close()
