from app.repositories import representative_repository


class RepresentativeService:

    @staticmethod
    def create_university(db, payload):
        obj = representative_repository.create_university(db, payload)

        return {
            "message": "Representative created successfully",
            "data": {
                "id": obj.id,
                "membership_id": obj.membership_id,
                "college_name": obj.college_name,
                "university_name": obj.university_name,
                "college_code": obj.college_code,
                "designation": obj.designation,
                "department": obj.department,
                "state": obj.state,
                "district": obj.district,
                "pincode": obj.pincode,
                "university_address": obj.university_address,
                "experience": obj.experience,
                "official_mail_id": obj.official_mail_id,
                "mobile_number": obj.mobile_number
            }
        }

    @staticmethod
    def create_autonomous(db, payload):
        obj = representative_repository.create_autonomous(db, payload)

        return {
            "message": "Representative created successfully",
            "data": {
                "id": obj.id,
                "membership_id": obj.membership_id,
                "college_name": obj.college_name,
                "college_code": obj.college_code,
                "designation": obj.designation,
                "department": obj.department,
                "state": obj.state,
                "district": obj.district,
                "pincode": obj.pincode,
                "college_address": obj.college_address,
                "experience": obj.experience,
                "official_mail_id": obj.official_mail_id,
                "mobile_number": obj.mobile_number
            }
        }

    @staticmethod
    def create_both(db, payload):
        obj = representative_repository.create_both(db, payload)

        return {
            "message": "Representative created successfully",
            "data": {
                "id": obj.id,
                "membership_id": obj.membership_id,
                "college_name": obj.college_name,
                "university_name": obj.university_name,
                "college_code": obj.college_code,
                "designation": obj.designation,
                "department": obj.department,
                "state": obj.state,
                "district": obj.district,
                "pincode": obj.pincode,
                "university_address": obj.university_address,
                "experience": obj.experience,
                "official_mail_id": obj.official_mail_id,
                "mobile_number": obj.mobile_number
            }
        }