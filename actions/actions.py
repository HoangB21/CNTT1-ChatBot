# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3

class ActionGetLecturerInfo(Action):
    def name(self) -> Text:
        return "action_get_lecturer_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        lecturer_name = next(tracker.get_latest_entity_values("lecturer_name"), None)
        lecturer_name = lecturer_name.title()
        print(lecturer_name)
        if lecturer_name:
            # Connect to the SQLite database
            conn = sqlite3.connect('./rasa_knowledge.db')
            cursor = conn.cursor()
            # Execute the query to fetch lecturer information
            cursor.execute("SELECT * FROM lecturers WHERE name=?", (lecturer_name,))
            lecturer_info = cursor.fetchone()

            if lecturer_info:
                # Extract lecturer details
                lecturer_id, lecturer_name, lecturer_email, lecturer_major, lecturer_research = lecturer_info

                # Respond with the lecturer's information
                dispatcher.utter_message(text=f"Thông tin giảng viên {lecturer_name}: Email: {lecturer_email}, Chuyên ngành: {lecturer_major}, Nghiên cứu: {lecturer_research}")
            else:
                dispatcher.utter_message(text="Xin lỗi, không tìm thấy thông tin cho giảng viên này.")

            # Close the connection to the database
            conn.close()
        else:
            dispatcher.utter_message(text="Xin lỗi, tôi không thể nhận dạng tên giảng viên trong câu hỏi của bạn.")

        return []