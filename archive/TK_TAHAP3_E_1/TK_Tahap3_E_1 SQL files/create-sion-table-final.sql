CREATE TABLE PENGGUNA (
  email          varchar(50)  not null,
  password       varchar(50)  not null,
  nama           varchar(100) not null,
  alamat_lengkap text         not null,
  primary key (email)
);

CREATE TABLE SPONSOR (
  email        varchar(50)  not null,
  logo_sponsor varchar(100) not null,
  primary key (email),
  foreign key (email) references PENGGUNA (email) on update cascade on delete cascade
);

CREATE TABLE DONATUR (
  email varchar(50) not null,
  saldo int         not null,
  primary key (email),
  foreign key (email) references PENGGUNA (email) on update cascade on delete cascade
);

CREATE TABLE RELAWAN (
  email         varchar(50) not null,
  no_hp         varchar(20) not null,
  tanggal_lahir date        not null,
  primary key (email),
  foreign key (email) references PENGGUNA (email) on update cascade on delete cascade
);

CREATE TABLE KEAHLIAN_RELAWAN (
  email    varchar(50) not null,
  keahlian varchar(50) not null,
  primary key (email, keahlian),
  foreign key (email) references relawan (email) on update cascade on delete cascade
);


CREATE TABLE ORGANISASI (
  email_organisasi  varchar(50) not null,
  website           varchar(50) not null,
  nama              varchar(50) not null,
  provinsi          varchar(50) not null,
  kabupaten_kota    varchar(50) not null,
  kecamatan         varchar(50) not null,
  kelurahan         varchar(50) not null,
  kode_pos          varchar(50) not null,
  status_verifikasi varchar(50) not null,
  primary key (email_organisasi)
);

CREATE TABLE PENGURUS_ORGANISASI (
  email      varchar(50) not null,
  organisasi varchar(50) not null,
  primary key (email),
  foreign key (email) references PENGGUNA (email) on update cascade on delete cascade,
  foreign key (organisasi) references organisasi (email_organisasi) on update cascade on delete cascade
);

create table tujuan_organisasi (
  organisasi varchar(50) not null,
  tujuan     text        not null,
  primary key (organisasi, tujuan),
  foreign key (organisasi) references organisasi (email_organisasi) on update cascade on delete cascade
);

create table relawan_organisasi (
  email_relawan varchar(50) not null,
  organisasi    varchar(50) not null,
  primary key (email_relawan, organisasi),
  foreign key (email_relawan) references relawan (email) on update cascade on delete cascade,
  foreign key (organisasi) references organisasi (email_organisasi) on update cascade on delete cascade
);

create table organisasi_terverifikasi (
  email_organisasi varchar(50) not null,
  nomor_registrasi varchar(50) not null,
  status_aktif     varchar(50) not null,
  primary key (email_organisasi),
  foreign key (email_organisasi) references organisasi (email_organisasi) on update cascade on delete cascade
);

create table donatur_organisasi (
  donatur    varchar(50) not null,
  organisasi varchar(50) not null,
  tanggal    date        not null,
  nominal    int         not null,
  primary key (donatur, organisasi),
  foreign key (donatur) references donatur (email) on update cascade on delete cascade,
  foreign key (organisasi) references organisasi_terverifikasi (email_organisasi) on update cascade on delete cascade
);

create table penilaian_performa (
  email_relawan varchar(50) not null,
  organisasi    varchar(50) not null,
  id            int         not null,
  deskripsi     text        not null,
  tgl_penilaian date        not null,
  nilai_skala   int         not null,
  primary key (email_relawan, organisasi, id),
  foreign key (email_relawan) references relawan (email) on update cascade on delete cascade,
  foreign key (organisasi) references organisasi_terverifikasi (email_organisasi) on update cascade on delete cascade
);

create table sponsor_organisasi (
  sponsor    varchar(50) not null,
  organisasi varchar(50) not null,
  tanggal    date        not null,
  nominal    int         not null,
  primary key (sponsor, organisasi),
  foreign key (sponsor) references sponsor (email) on update cascade on delete cascade,
  foreign key (organisasi) references organisasi_terverifikasi (email_organisasi) on update cascade on delete cascade
);

create table kegiatan (
  kode_unik            varchar(20) not null,
  organisasi_perancang varchar(50) not null,
  judul                varchar(50) not null,
  dana_dibutuhkan      int         not null,
  tanggal_mulai        date        not null,
  tanggal_selesai      date        not null,
  deskripsi            text        not null,
  primary key (kode_unik),
  foreign key (organisasi_perancang) references organisasi_terverifikasi (email_organisasi) on update cascade on delete cascade
);

CREATE TABLE LAPORAN_KEUANGAN (
  organisasi        VARCHAR(50) NOT NULL,
  tgl_dibuat        date        NOT NULL,
  rincian_pemasukan TEXT        NOT NULL,
  total_pemasukan   INT         NOT NULL,
  total_pengeluaran INT         NOT NULL,
  is_disetujui      BOOLEAN     NOT NULL,
  PRIMARY KEY (organisasi, tgl_dibuat),
  FOREIGN KEY (organisasi) REFERENCES ORGANISASI_TERVERIFIKASI (email_organisasi) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE BERITA (
  kode_unik    VARCHAR(50)  NOT NULL,
  kegiatan     VARCHAR(50)  NOT NULL,
  judul        VARCHAR(100) NOT NULL,
  deskripsi    TEXT         NOT NULL,
  tgl_update   DATE         NOT NULL,
  tgl_kegiatan DATE         NOT NULL,
  PRIMARY KEY (kode_unik),
  FOREIGN KEY (kegiatan) REFERENCES KEGIATAN (kode_unik) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE REWARD (
  kode_kegiatan VARCHAR(50) NOT NULL,
  barang_reward VARCHAR(50) NOT NULL,
  harga_min     INT         NOT NULL,
  harga_max     INT         NOT NULL,
  PRIMARY KEY (kode_kegiatan, barang_reward),
  FOREIGN KEY (kode_kegiatan) REFERENCES KEGIATAN (kode_unik) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE KATEGORI (
  kode VARCHAR(20) NOT NULL,
  nama VARCHAR(50) NOT NULL,
  PRIMARY KEY (kode)
);

CREATE TABLE KATEGORI_KEGIATAN (
  kode_kegiatan VARCHAR(50) NOT NULL,
  kode_kategori VARCHAR(20) NOT NULL,
  PRIMARY KEY (kode_kegiatan, kode_kategori),
  FOREIGN KEY (kode_kegiatan) REFERENCES KEGIATAN (kode_unik) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (kode_kategori) REFERENCES KATEGORI (kode) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE DONATUR_KEGIATAN (
  donatur  VARCHAR(50) NOT NULL,
  kegiatan VARCHAR(50) NOT NULL,
  tanggal  DATE        NOT NULL,
  nominal  INT         NOT NULL,
  PRIMARY KEY (donatur, kegiatan),
  FOREIGN KEY (donatur) REFERENCES DONATUR (email) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (kegiatan) REFERENCES KEGIATAN (kode_unik) ON UPDATE CASCADE ON DELETE CASCADE
);