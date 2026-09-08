-- ============================================================
-- ms-usuarios | Datos de prueba para el avance del 50%
-- ============================================================
-- Password de todos: condominio123
-- (data de desarrollo, no una credencial real)
--
-- Los residente_id corresponden a los residentes del seed de ms-residentes.
-- ============================================================

INSERT INTO usuarios (residente_id, email, password_hash, rol) VALUES
  (NULL, 'admin@condominio.com',        '$2b$12$k2l7LY/mmNy6g2MddikGjeUoTtWIAkUJ0fgGaEJilFBlkljn12lna', 'ADMIN'),
  (1,    'lucia.vargas@example.com',    '$2b$12$k2l7LY/mmNy6g2MddikGjeUoTtWIAkUJ0fgGaEJilFBlkljn12lna', 'RESIDENTE'),
  (4,    'ricardo.salazar@example.com', '$2b$12$k2l7LY/mmNy6g2MddikGjeUoTtWIAkUJ0fgGaEJilFBlkljn12lna', 'RESIDENTE'),
  (5,    'teresa.ampuero@example.com',  '$2b$12$k2l7LY/mmNy6g2MddikGjeUoTtWIAkUJ0fgGaEJilFBlkljn12lna', 'RESIDENTE');

INSERT INTO sesiones (usuario_id, ip_origen, user_agent, exitoso) VALUES
  (1, '192.168.1.10', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', TRUE),
  (2, '192.168.1.24', 'Mozilla/5.0 (X11; Linux x86_64)',           TRUE),
  (2, '192.168.1.24', 'Mozilla/5.0 (X11; Linux x86_64)',           FALSE),
  (3, '10.0.0.7',     'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0)',  TRUE);
