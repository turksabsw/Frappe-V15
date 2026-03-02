frappe.ui.form.on("Daily Checkin", {
  refresh(frm) {

    frm.disable_save();
    frm.clear_custom_buttons();

    // -----------------------------
    // YENİ KAYIT → GİRİŞ YAP
    // -----------------------------
    if (frm.is_new()) {
      frm.add_custom_button("Giriş Yap", () => {

        frm.set_value("status", "Checked In");
        frm.set_value("check_in_time", frappe.datetime.now_datetime());

        frm.save().then(() => {
          frappe.show_alert("Giriş yapıldı");
          frm.reload_doc();   // 🔥 refresh'i tekrar tetikler
        });

      }).addClass("btn-primary");
    }

    // -----------------------------
    // CHECKED IN → ÇIKIŞ YAP
    // -----------------------------
    if (!frm.is_new() && frm.doc.status === "Checked In") {
      frm.add_custom_button("Çıkış Yap", () => {

        frm.set_value("check_out_time", frappe.datetime.now_datetime());
        frm.set_value("status", "Checked Out");

        frm.save().then(() => {
          frappe.show_alert("Çıkış yapıldı");
          frm.reload_doc();
        });

      }).addClass("btn-danger");
    }
  }
});
