from _future_ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, date

from base import Patient, PatientBaseInfo, PatientStatus

@dataclass
class Allergy:
    name: str
    severity: str  
    note: str = ""

@dataclass
class MedicalRecordEntry:
    when: datetime
    description: str
    doctor: str

@dataclass
class MedicalRecord:
    patient_id: str
    entries: List[MedicalRecordEntry] = field(default_factory=list)


    def add_entry(self, description: str, doctor: str) -> None:
        self.entries.append(MedicalRecordEntry(datetime.now(), description, doctor))

    @staticmethod
    def summarize(entries: List[MedicalRecordEntry]) -> str:
        return f"Toplam {len(entries)} kayıt"

    @classmethod
    def empty_for(cls, patient_id: str) -> "MedicalRecord":
        return cls(patient_id=patient_id)

@dataclass
class VisitHistoryItem:
    visit_date: date
    department: str
    notes: str = ""

@dataclass
class VisitHistory:
    patient_id: str
    visits: List[VisitHistoryItem] = field(default_factory=list)

    def add_visit(self, department: str, notes: str = "") -> None:
        self.visits.append(VisitHistoryItem(date.today(), department, notes))

    @staticmethod
    def last_visit_department(visits: List[VisitHistoryItem]) -> Optional[str]:
        return visits[-1].department if visits else None

    @classmethod
    def empty_for(cls, patient_id: str) -> "VisitHistory":
        return cls(patient_id=patient_id)



class Inpatient(Patient):
    """Yatan hasta: oda ve yatış tarihi bilgisi içerir."""

    def _init_(self, base: PatientBaseInfo, room_number: str, admission_date: date):
        super()._init_(base)
        self.room_number = room_number
        self.admission_date = admission_date
        self.allergies: List[Allergy] = []
        self.record = MedicalRecord.empty_for(base.id)
        self.visits = VisitHistory.empty_for(base.id)

    def get_info(self) -> str:
        return (f"[Inpatient] {self.base.name} | Oda: {self.room_number} | "
                f"Yatış: {self.admission_date.isoformat()} | Durum: {self.base.status}")

    def update_status(self, new_status: str) -> None:
        if new_status == PatientStatus.DISCHARGED:
            self.record.add_entry("Taburcu özeti oluşturuldu", doctor="Servis Doktoru")
        self.base.status = new_status

    def change_room(self, new_room: str) -> None:
        self.room_number = new_room

    @staticmethod
    def is_long_stay(admission_date: date, threshold_days: int = 10) -> bool:
        return (date.today() - admission_date).days >= threshold_days

    @classmethod
    def create_default(cls, base: PatientBaseInfo) -> "Inpatient":
        return cls(base=base, room_number="Z-101", admission_date=date.today())

class Outpatient(Patient):
    """Ayakta (poliklinik) hasta: randevu tarihi içerir."""

    def _init_(self, base: PatientBaseInfo, appointment_date: date):
        super()._init_(base)
        self.appointment_date = appointment_date
        self.record = MedicalRecord.empty_for(base.id)
        self.visits = VisitHistory.empty_for(base.id)

    def get_info(self) -> str:
        return (f"[Outpatient] {self.base.name} | Randevu: {self.appointment_date.isoformat()} | "
                f"Durum: {self.base.status}")

    def update_status(self, new_status: str) -> None:
        self.visits.add_visit("Poliklinik", notes=f"Durum {self.base.status} -> {new_status}")
        self.base.status = new_status

    def reschedule(self, new_date: date) -> None:
        self.appointment_date = new_date

    @staticmethod
    def needs_followup(record: MedicalRecord) -> bool:
    
        return len(record.entries) < 3

    @classmethod
    def create_for_today(cls, base: PatientBaseInfo) -> "Outpatient":
        return cls(base=base, appointment_date=date.today())

class EmergencyPatient(Patient):
    """Acil hasta: triyaj seviyesi ve varış zamanı içerir."""

    def _init_(self, base: PatientBaseInfo, triage_level: int, arrival_time: datetime):
        super()._init_(base)
        self.triage_level = triage_level 
        self.arrival_time = arrival_time
        self.record = MedicalRecord.empty_for(base.id)
        self.visits = VisitHistory.empty_for(base.id)

    def get_info(self) -> str:
        return (f"[Emergency] {self.base.name} | Triyaj: {self.triage_level} | "
                f"Geliş: {self.arrival_time.isoformat()} | Durum: {self.base.status}")

    def update_status(self, new_status: str) -> None:
        if self.triage_level == 1 and new_status == PatientStatus.DISCHARGED:
            self.record.add_entry("Acil kritik vaka taburcu notu", doctor="Acil Hekimi")
        self.base.status = new_status

    def escalate(self) -> None:
        """Triyaj seviyesini acil ihtiyaç halinde düşür (daha kritik)."""
        self.triage_level = max(1, self.triage_level - 1)

    @staticmethod
    def is_critical(triage_level: int) -> bool:
        return triage_level in (1, 2)

    @classmethod
    def admit_from_ambulance(cls, base: PatientBaseInfo) -> "EmergencyPatient":
        return cls(base=base, triage_level=2, arrival_time=datetime.now())