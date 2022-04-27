# USE infoautoPRO2;

CREATE OR REPLACE VIEW lead_util_view AS
  SELECT lead.id as id,
         CASE
           WHEN (lead.result IS NULL) OR (
             (lead.result IS NOT NULL) AND (lead.result NOT LIKE 'wrong') AND (lead.result NOT LIKE 'unreachable')
             ) THEN TRUE
           ELSE FALSE
             END as lead_util
  FROM leads_lead as lead;

CREATE OR REPLACE VIEW lead_atendidos_view AS
  SELECT lead.id as id,
         CASE
           WHEN (lead_util.lead_util IS TRUE) AND (lead.status NOT LIKE 'new') AND (lead.status NOT LIKE 'pending')
                   THEN TRUE ELSE FALSE
             END lead_atendidos
  FROM leads_lead lead
         LEFT JOIN lead_util_view lead_util on lead_util.id=lead.id;

CREATE OR REPLACE VIEW lead_cerrados_view AS
  SELECT lead.id as id, CASE
      WHEN (lead_atendidos.lead_atendidos is TRUE) AND (lead.result IS NOT NULL) AND (lead.status LIKE 'end')
                                  THEN TRUE ELSE FALSE
      END lead_cerrados
  FROM leads_lead lead
         LEFT JOIN lead_atendidos_view lead_atendidos on lead_atendidos.id=lead.id;

CREATE OR REPLACE VIEW lead_disponible_view AS
  SELECT lead.id as id, CASE
      WHEN (lead_cerrados.lead_cerrados IS TRUE) AND ((lead.result NOT LIKE 'not_available') OR (lead.result IS NULL))
                                  THEN TRUE ELSE FALSE
      END lead_disponible
  FROM leads_lead lead
         LEFT JOIN lead_cerrados_view lead_cerrados on lead_cerrados.id=lead.id;

CREATE OR REPLACE VIEW vendido_reservado_view as
  SELECT lead.id as id,
         CASE
           WHEN (lead_disponible.lead_disponible IS TRUE) AND (lead.result LIKE 'reserved_vehicle') THEN TRUE ELSE FALSE
             END as reservado
  FROM leads_lead lead
  LEFT JOIN lead_disponible_view lead_disponible on lead_disponible.id = lead.id;

CREATE OR REPLACE VIEW tmrs_view as
  SELECT task.type as type,
         AVG(ABS(TIMESTAMPDIFF(SECOND, task.planified_realization_date, task.realization_date))) AS NSA
  from leads_task as task
  group by task.type;

-- CREATE OR REPLACE VIEW
--   MASTER_USERS_VIEW AS
--   SELECT user_table.first_name as "Nombre", user_table.last_name as "Apellidos", user_table.email as "Email",
--          user_session.start_working as "Ultimo Inicio de Sesion", user_session.end_working as "Ultimo Cierre de Sesion",
--          user_table.user_activation_date as "Fecha de Alta en Plataforma",
--          user_table.user_deactivation_date as "Fecha de Baja en Plataforma",
--          user_session.worked_hours as "Horas Trabajadas Ayer"
--   FROM users_sessionwithhistoric user_session
--          LEFT JOIN users_user user_table on user_session.user_id = user_table.id;

CREATE OR REPLACE VIEW task_view AS
  SELECT
         lead.id as id,
         tmrs.NSA as "Tiempo realizacion solicitudes",
         CASE
           WHEN lead.status like 'pending' or lead.status like 'commercial_management' THEN true ELSE false
             END AS "Tareas pendientes",
         ABS(TIMESTAMPDIFF(SECOND, task.planified_realization_date, task.realization_date)) as asa_tareas,
         ABS(TIMESTAMPDIFF(SECOND, task.planified_tracking_date, task.tracking_date)) as asa_seguimiento,
         CASE
           WHEN task.realization_date_check is false and task.planified_realization_date is not null
                   THEN task.planified_realization_date ELSE NULL
             END as tarea_programada,
         CASE
           WHEN task.realization_date_check is true and task.realization_date is not null
                   THEN task.realization_date ELSE NULL
             END as tarea_realizada,
         CASE
           WHEN task.tracking_date_check is false and task.planified_tracking_date is not null
                   THEN task.planified_tracking_date ELSE NULL
             END as seguimiento_programado,
         CASE
           WHEN task.tracking_date_check is true and task.tracking_date is not null THEN task.tracking_date ELSE NULL
             END as seguimiento_realizado
  FROM leads_lead lead
         LEFT JOIN leads_request request on lead.request_id = request.id
         LEFT JOIN leads_request_task lrt on request.id = lrt.request_id
         LEFT JOIN leads_task task on lrt.task_id = task.id
         LEFT JOIN tmrs_view tmrs ON tmrs.type = task.type;

