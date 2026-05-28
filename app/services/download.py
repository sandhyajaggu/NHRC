import pandas as pd
from io import BytesIO

from fastapi.responses import StreamingResponse

from app.models.event_registration import EventRegistration


class DownloadService:

    @staticmethod
    def download_registrations_excel(db, event_id: int):

        registrations = db.query(EventRegistration).filter(
            EventRegistration.event_id == event_id
        ).all()

        data = []

        for reg in registrations:

            data.append({
                "Candidate Name": reg.full_name,
                "Email": reg.email,
                "Phone": reg.phone_number,
                "NHRC ID": reg.nhrc_id,
                "Role": reg.role,
                "Status": reg.status,
                "Location": reg.location
            })

        df = pd.DataFrame(data)

        output = BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(
                writer,
                index=False,
                sheet_name="Registrations"
            )

        output.seek(0)

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition":
                f"attachment; filename=event_{event_id}_registrations.xlsx"
            }
        )