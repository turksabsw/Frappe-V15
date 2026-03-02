import frappe
from frappe.model.document import Document
from frappe.utils import getdate, get_datetime, now_datetime


class DailyCheckin(Document):

    # --------------------------------------------------
    # LIFECYCLE
    # --------------------------------------------------

    def before_insert(self):
        self.ensure_user_email()
        self.ensure_check_in_time()
        self.ensure_date()
        self.ensure_initial_status()

    def before_save(self):
        self.ensure_user_email()
        self.ensure_date()
        self.ensure_work_duration()

    # --------------------------------------------------
    # CORE
    # --------------------------------------------------

    def ensure_user_email(self):
        # Kullanıcıdan otomatik doldur
        if not self.user_email:
            self.user_email = frappe.session.user

    def ensure_check_in_time(self):
        # İlk insert sırasında giriş zamanı yoksa set et
        if not self.check_in_time:
            self.check_in_time = now_datetime()

    def ensure_date(self):
        # Gün bazlı raporlar için
        if not self.date:
            base_time = self.check_in_time or now_datetime()
            self.date = getdate(base_time)

    def ensure_initial_status(self):
        # İlk kayıt her zaman Checked In
        if not self.status:
            self.status = "Checked In"

    def ensure_work_duration(self):
        # Çıkış yoksa süre hesaplama
        if not self.check_in_time or not self.check_out_time:
            return

        in_time = get_datetime(self.check_in_time)
        out_time = get_datetime(self.check_out_time)

        if out_time < in_time:
            frappe.throw("Çıkış zamanı, giriş zamanından önce olamaz.")

        diff = out_time - in_time
        self.work_duration_minutes = int(diff.total_seconds() / 60)
