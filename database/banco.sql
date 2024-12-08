CREATE TABLE IF NOT  EXISTS tb_usuarios (
    usu_id INTEGER PRIMARY KEY AUTOINCREMENT,
    usu_nome TEXT NOT NULL,
    usu_senha TEXT NOT NULL,
    usu_email TEXT NOT NULL
);
