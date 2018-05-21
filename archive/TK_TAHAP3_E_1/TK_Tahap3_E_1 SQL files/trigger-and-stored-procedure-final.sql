CREATE OR REPLACE FUNCTION saldo_donatur()
  RETURNS "trigger" AS
$$
BEGIN
  IF (TG_OP = 'INSERT')
  THEN
    UPDATE donatur
    SET saldo =
    saldo - NEW.nominal
    WHERE email = NEW.donatur;
    RETURN NEW;

  ELSIF (TG_OP = 'UPDATE')
    THEN
      UPDATE donatur
      SET saldo =
      saldo + OLD.nominal
      WHERE email = OLD.donatur;
      UPDATE donatur
      SET saldo =
      saldo - NEW.nominal
      WHERE email = NEW.donatur;
      RETURN NEW;

  ELSEIF (TG_OP = 'DELETE')
    THEN
      UPDATE donatur
      SET saldo =
      saldo + OLD.nominal
      WHERE email = OLD.donatur;
      RETURN OLD;
  END IF;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER saldo_donatur_kegiatan
  AFTER INSERT OR UPDATE OR DELETE
  ON DONATUR_KEGIATAN
  FOR EACH ROW
EXECUTE PROCEDURE saldo_donatur();

CREATE TRIGGER saldo_donatur_organisasi
  AFTER INSERT OR UPDATE OR DELETE
  ON DONATUR_ORGANISASI
  FOR EACH ROW
EXECUTE PROCEDURE saldo_donatur();

CREATE OR REPLACE FUNCTION status_aktif_organisasi()
  RETURNS trigger AS
$$
BEGIN
  IF (NEW.is_disetujui = false)
  THEN
    UPDATE ORGANISASI_TERVERIFIKASI
    SET status_aktif =
    'tidak aktif'
    WHERE email_organisasi = NEW.organisasi;
  ELSE IF (NEW.is_disetujui = true)
  THEN
    UPDATE ORGANISASI_TEVERIFIKASI
    SET status_aktif =
    'aktif'
    WHERE email_organisasi = NEW.organisasi;
  end if;
  END IF;
  RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER status_aktif_organisasi
  AFTER UPDATE
  ON LAPORAN_KEUANGAN
  FOR EACH ROW
EXECUTE PROCEDURE status_aktif_organisasi();
