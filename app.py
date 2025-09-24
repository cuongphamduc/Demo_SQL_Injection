from fastapi import FastAPI, Path, HTTPException, Query
import sqlite3, uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is working!"}

# SAFE function - original code
def get_student_from_db(student_id: int):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    # SAFE: use parameter binding, not string concatenation
    cursor.execute("SELECT name, age FROM students WHERE id = ?", (student_id,))
    result = cursor.fetchone()
    conn.close()
    return result


# UNSAFE function - for SQL injection demo
def get_student_from_db_unsafe(student_id_str: str):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    # DANGEROUS: direct string concatenation - vulnerable to SQL injection
    query = f"SELECT name, age FROM students WHERE id = {student_id_str}"
    print(f"[UNSAFE] Executing: {query}")  # Debug to see the query
    try:
        cursor.execute(query)
        result = cursor.fetchall()  # Use fetchall to see multiple results
        conn.close()
        return result
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail=f"SQL Error: {str(e)}")


# SAFE endpoint - original code
@app.get("/students/{student_id}")
def get_student(student_id: int = Path(..., ge=1)):
    student = get_student_from_db(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"id": student_id, "name": student[0], "age": student[1]}


# UNSAFE endpoint - for SQL injection demo
@app.get("/students-unsafe/")
def get_student_unsafe(student_id: str = Query(..., description="Student ID (unsafe for demo)")):
    results = get_student_from_db_unsafe(student_id)
    if not results:
        raise HTTPException(status_code=404, detail="No student found")

    students = []
    for result in results:
        students.append({"name": result[0], "age": result[1]})

    return {
        "results": students,
        "warning": "⚠️ UNSAFE endpoint - for SQL injection demo only!",
        "examples": {
            "normal": "?student_id=1",
            "sql_injection": "?student_id=1 OR 1=1"
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)