import csv
import io
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import get_db
from models.assignment import Assignment
from models.shift import Shift
from models.user import User
from services.auth_service import get_current_user

router = APIRouter()

@router.get("/export/shifts")
def export_shifts(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")

    rows = (
        db.query(User, Shift, Assignment)
        .join(Assignment, Assignment.user_id == User.id)
        .join(Shift, Shift.id == Assignment.shift_id)
        .all()
    )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["First Name", "Last Name", "Shift Date", "Facility", "Start Time", "End Time", "Active"])

    for user, shift, assignment in rows:
        writer.writerow([
            user.first_name,
            user.last_name,
            shift.shift_date,
            shift.facility_name,
            shift.start_time,
            shift.end_time,
            assignment.is_active
        ])
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=shifts_export.csv"}
    )