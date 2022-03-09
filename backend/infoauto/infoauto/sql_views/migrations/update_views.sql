CREATE OR REPLACE VIEW
    MASTER_INFOAUTO_VIEW_CHANNEL_PHONE AS
SELECT
    lead.id,
    ifnull( nlc.is_duplicated, 0) as "dd", -- Duplicado
    concessionaire.name as "Nombre de la concesion",
    o.name as "Origen",
    scc.name as "Medio",
    o2.name as "Origen publicidad",
    lead.channel2_id is not null as "Exposicion",
    concat(uu.first_name, ' ',uu.last_name) as "Asignado a",
    DATE_FORMAT(CONVERT_TZ(lead.incoming_call_datetime, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') as "Fecha llamada entrante",
    CASE
        WHEN nlc.is_duplicated = 1 THEN 'Lead cerrado'
        WHEN lead.status like 'new' THEN 'Lead no atendido'
        WHEN lead.status like 'attended' THEN 'Lead atendido por comercial '
        WHEN lead.status like 'commercial_management' THEN 'Tareas pendientes'
        WHEN lead.status like 'pending' THEN 'Tareas Pendientes'
        WHEN lead.status like 'tracing' THEN 'Seguimiento'
        WHEN lead.status like 'end' THEN 'Lead cerrado'
        END as "Estado",
    CASE
        WHEN nlc.is_duplicated = 1 THEN 'Descartado'
        WHEN lead.result = 'not_available' then 'Descartado'
        WHEN lead.result = 'negative' then 'Descartado'
        WHEN lead.result = 'reserved_vehicle' then 'Ganado'
        WHEN lead.result = 'unreachable' then 'Descartado'
        WHEN lead.result = 'wrong' then 'Descartado'
        WHEN lead.result = 'positive' then 'Ganado'
        WHEN lead.result = 'error' then 'Descartado'
        END as "Resultado",
    lead.result_reason as "Motivo resultado",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        WHEN client2.client_type = 'private' then 'Particular'
        WHEN client2.client_type = 'freelance' then 'Autonomo'
        WHEN client2.client_type = 'company' then 'Empresa'
        ELSE client2.client_type
        END as "Tipo cliente",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE client2.identification
        END as "Identificador cliente",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE client2.name
        END as "Nombre cliente",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE client2.business_name
        END as "Razon social cliente",
    client2.phone as "Telefono",
    client2.desk_phone as "Telefono fijo",
    client2.email as "Email",
    client2.postal_code as "Codigo postal",
    client2.address1 as "Direccion cliente",
    client2.address2 as "Direccion cliente 2",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE locality.name
        END as "Localidad",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE province.name
        END as "Provincia",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE v.brand_model
        END as "Vehiculo demandado Marca",
    CASE
        WHEN nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE v.model
        END as "Vehiculo demandado Modelo",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE v.price
        END as "Vehiculo demandado precio",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE v.km
        END as "Vehiculo demandado kilometro",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE v.year
        END as "Vehiculo demandado anio",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE gastype.name
        END as "Vehiculo demandado combustible",
    CASE
        WHEN nlc.is_duplicated = 1 or  lead.result = 'wrong' THEN  NULL
        ELSE v.vehicle_type
        END as "Vehiculo demandado tipo",
    CASE
        WHEN nlc.is_duplicated = 1 or  lead.result = 'wrong' THEN  NULL
        ELSE v.comercial_category
        END as "Vehiculo demandado categoria comercial",
    CASE
        WHEN nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE v.power
        END as "Vehiculo demandado potencia",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE v.gear_shift
        END as "Vehiculo demandado tipo caja cambios",
    CASE
        WHEN nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE v.ad_link
        END as "Vehiculo demandado link anuncio",
    actual_vehicle.brand as "Marca vehiculo actual",
    actual_vehicle.model as "Modelo vehiculo actual",
    actual_vehicle.version as "Version vehiculo actual",
    actual_vehicle.km as "Kilometros vehiculo actual",
    actual_vehicle.status as "Estado vehiculo actual",
    actual_vehicle.features as "Acabados vehiculo actual",
    actual_vehicle.evaluation_vo_price as "Precio evaluacion VO vehiculo actual",
    actual_vehicle.total_vehicles as "Numero vehiculos total flota",
    actual_vehicle.total_comercial_vehicles as "Numero vehiculos comerciales flota",
    actual_vehicle.total_tourism_vehicles as "Numero vehiculos turismos flota",
    actual_vehicle.fleet_notes as "Notas flota",
    actual_vehicle.license_plate as "Matricula vehiculo actual",
    DATE_FORMAT(CONVERT_TZ(actual_vehicle.buy_date, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')  as "Fecha compra vehiculo actual",
    DATE_FORMAT(CONVERT_TZ(actual_vehicle.registration_date, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')  as "Fecha matriculacion vehiculo actual",
    DATE_FORMAT(CONVERT_TZ(actual_vehicle.last_mechanic_date, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')  as "Fecha ultimo taller vehiculo actual",
    actual_vehicle.cv as "Caballos vehiculo actual",
    actual_vehicle.is_finance as "Vehiculo actual es financiado",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE GROUP_CONCAT(DISTINCT n.content
                          ORDER BY n.created ASC
                          SEPARATOR '\n')
        END as "Notas",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE lead.score
        END as "Probabilidad de compra",
    CASE
        WHEN lead.before_reactivated_result = 'not_available' then 'No disponible'
        WHEN lead.before_reactivated_result = 'negative' then 'Descartado'
        WHEN lead.before_reactivated_result = 'reserved_vehicle' then 'Vehiculo reservado'
        WHEN lead.before_reactivated_result = 'unreachable' then 'Ilocalizable'
        WHEN lead.before_reactivated_result = 'wrong' then 'Duplicado'
        END as "Resultado historico",
    lead.is_reactivated as "Reactivado",
    DATE_FORMAT(CONVERT_TZ(lead.created, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')  as "Fecha de alta",
    1 as "LEAD RECIBIDO",
    CASE
        WHEN (lead.status='end' and lead.result_reason in ('duplicado', 'ilocalizable', 'informacion_cliente_incorrecta', 'publicidad', 'error', 'otro_departamento'))  THEN  0
        ELSE 1
        END as "LEAD UTIL",
    CASE
        WHEN (lead.result_reason not in ('duplicado', 'ilocalizable', 'informacion_cliente_incorrecta', 'publicidad', 'error', 'otro_departamento') or lead.result_reason is null)  and lead.status = 'end' THEN  1
        ELSE 0
        END as "CERRADOS",
    CASE
        WHEN (lead.result_reason not in ('duplicado', 'ilocalizable', 'informacion_cliente_incorrecta', 'publicidad', 'error', 'otro_departamento' 'vehiculo_ya_vendido') or lead.result_reason is null)  and lead.status = 'end' THEN  1
        ELSE 0
        END as "DISPONIBLE",
    CASE
        WHEN (lead.result_reason is null or lead.result_reason not in ('duplicado', 'ilocalizable', 'informacion_cliente_incorrecta', 'publicidad', 'error', 'otro_departamento' 'vehiculo_ya_vendido')) and lead.status = 'end' and lead.result in ('positive', 'reserved_vehicle') THEN  1
        ELSE 0
        END  as "VENDIDO/RESERVADO",
    CASE
        WHEN (SELECT count(*) FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0) > 0 THEN true
        ELSE false
        END AS "Tareas pendientes",
    -- uu.user_activation_date as "Alta usuario",
    -- uu.user_deactivation_date as "Baja usuario"
    (select min(created) from leads_leadwhatsappmessage where lead_id=lead.id) as 'Primer Whatsapp',
    (select max(created) from leads_leadwhatsappmessage where lead_id=lead.id) as 'Ultimo Whatsapp',
    (select count(*) from leads_leadwhatsappmessage where lead_id=lead.id) as 'Numero Whatsapp',
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.outgoing_call_datetime, 'UTC', 'Europe/Madrid'),  '%d/%m/%Y %H:%i:%s')
        END as "Fecha llamada saliente",
    CASE
        WHEN nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        WHEN lead.status_call = 'undefined' then 'Desconocido'
        WHEN lead.status_call = 'attended' then 'Atendido'
        WHEN lead.status_call = 'not_attended' then 'No atendido'
        WHEN lead.status_call = 'out_of_working_hours' then 'Fuera de horario laboral'
        END as "Status call",
    DATE_FORMAT(CONVERT_TZ(lead.incoming_email_datetime, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s') AS "Fecha email entrante", -- TODO
    DATE_FORMAT(CONVERT_TZ(lead.outgoing_email_datetime, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s') AS "Fecha email saliente", -- TODO
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.status_new_datetime, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')
        END as "Fecha lead no atendido",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.status_pending_datetime, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')
        END as "Fecha tareas pendientes",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.status_attended_datetime, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')
        END as "Fecha lead atendido",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.status_tracing_datetime, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')
        END as "Fecha lead en seguimiento",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.status_end_datetime, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')
        END as "Fecha cierre lead",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.reactivated_date, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')
        END as "Fecha reactivacion lead",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE lead.threshold_concession_call / 60
        END as "TUmbral concesion llamadas",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE lead.threshold_concession_email / 60
        END as "TUmbral concesion email",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE lead.computed_call_asa / 60
        END as "ASA LLAMADAS",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        ELSE lead.computed_email_asa / 60
        END as "ASA EMAIL",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        WHEN lead.computed_call_asa > lead.threshold_concession_call then 1
        WHEN lead.computed_call_asa <= lead.threshold_concession_call then 0
        END as "Tumbral llamada superado",
    CASE
        WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
        WHEN lead.computed_email_asa > lead.threshold_concession_email then 1
        WHEN lead.computed_email_asa <= lead.threshold_concession_email then 0
        END as "Tumbral email superado",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(planified_realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0 ORDER BY planified_realization_date LIMIT 1
    ) AS "Fecha primera tarea programada",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(planified_realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0 ORDER BY  planified_realization_date DESC LIMIT 1
    ) AS "Fecha ultima tarea programada",
    (
        SELECT count(*) FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0
    ) as "Numero tarea programada",
    -- Tareas realizadas.
    (
        SELECT DATE_FORMAT(CONVERT_TZ(realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0  ORDER BY  realization_date DESC LIMIT 1
    ) AS "Fecha primera tarea realizada",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s')  FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0  ORDER BY  realization_date  LIMIT 1
    ) AS "Fecha ultima tarea realizada",
    (
        SELECT count(*) FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0
    ) AS "Numero de tareas programadas",
    (
        SELECT count(*) FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0 and realization_date is not null
    ) as "Numero de tareas realizadas",
    -- Seguimientos realizados
    (
        SELECT DATE_FORMAT(CONVERT_TZ(planified_realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 1 ORDER BY planified_realization_date LIMIT 1
    ) AS "Fecha primer seguimiento a programado",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(planified_realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 1 ORDER BY  planified_realization_date DESC LIMIT 1
    ) AS "Fecha ultima seguimiento a programado",
    (
        SELECT count(*) FROM leads_task WHERE lead_id=lead.id and is_traking_task = 1
    ) as "Numero seguimientos programados",
    -- Seguimientos realizados
    (
        SELECT DATE_FORMAT(CONVERT_TZ(realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 1 ORDER BY planified_realization_date LIMIT 1
    ) AS "Fecha primer seguimiento realizado",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 1 ORDER BY  planified_realization_date DESC LIMIT 1
    ) AS "Fecha ultimo seguimiento realizado",
    (
        SELECT count(*) FROM leads_task WHERE lead_id=lead.id and is_traking_task = 1 and realization_date is not null
    ) as "Numero de seguimientos realizados",
    -- Llamadas
    (
        SELECT DATE_FORMAT(CONVERT_TZ(nc.created, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM netelip_leads_callcontrolleadmodel as c
                                                                                                         INNER JOIN netelip_callcontrolmodel nc on c.call_control_id = nc.id
        WHERE c.lead_id=lead.id and nc.call_origin='user' ORDER BY nc.created
        LIMIT 1
    ) as "Fecha primera llamada cliente realizada",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(nc.created, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM netelip_leads_callcontrolleadmodel as c
                                                                                                         INNER JOIN netelip_callcontrolmodel nc on c.call_control_id = nc.id
        WHERE c.lead_id=lead.id and nc.call_origin='user' ORDER BY nc.created desc
        LIMIT 1
    ) as "Fecha ultima llamada cliente realizada",
    (
        SELECT count(*) FROM netelip_leads_callcontrolleadmodel as c
                                 INNER JOIN netelip_callcontrolmodel nc on c.call_control_id = nc.id
        WHERE c.lead_id=lead.id and nc.call_origin='user'
    ) as "Numero de llamadas realizadas",
    -- Email
    (
        SELECT DATE_FORMAT(CONVERT_TZ(created, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_leadmanagement WHERE message like '%Email enviado%' and lead_id=lead.id order by  created LIMIT 1
    ) as "Fecha primera mail enviado",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(created, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_leadmanagement WHERE message like '%Email enviado%' and lead_id=lead.id order by created desc LIMIT 1
    ) as "Fecha ultimo mail enviado",
    (
        SELECT count(*) FROM leads_leadmanagement WHERE message like '%Email enviado%' and lead_id=lead.id order by created desc
    ) as "Numero de mails enviados",
    lead.concessionaire_id,
    lead.created,
    lead.user_id
FROM leads_lead lead
             LEFT JOIN leads_concessionaire concessionaire on lead.concessionaire_id = concessionaire.id
             LEFT JOIN source_channels_source scs on lead.source_id = scs.id
             LEFT JOIN leads_origin o on scs.origin_id = o.id
             LEFT JOIN source_channels_channel scc on scs.channel_id = scc.id
             LEFT JOIN leads_origin o2 on lead.origin2_id = o2.id
             LEFT JOIN leads_client client2 on lead.client_id = client2.id
             LEFT JOIN countries_province province on client2.province_id = province.id
             LEFT JOIN countries_locality locality on client2.location_id = locality.id
             LEFT JOIN leads_vehicle v on v.lead_id = lead.id
             LEFT JOIN leads_appraisal actual_vehicle on actual_vehicle.lead_id = lead.id
             LEFT JOIN leads_gastype gastype on v.gas_id = gastype.id
             LEFT JOIN leads_lead_note lln on lead.id = lln.lead_id
             LEFT JOIN leads_note n on lln.note_id = n.id
             LEFT JOIN users_user uu on lead.user_id = uu.id
             LEFT JOIN lead_util_view lead_util on lead.id = lead_util.id
             LEFT JOIN lead_cerrados_view lead_cerrados on lead.id = lead_cerrados.id
             LEFT JOIN lead_disponible_view lead_disponible on lead.id = lead_disponible.id
             LEFT JOIN vendido_reservado_view vendido_reservado on vendido_reservado.id = lead.id
             LEFT JOIN netelip_leads_callcontrolleadmodel nlc on lead.id = nlc.lead_id and nlc.is_duplicated = 0
             LEFT JOIN netelip_callcontrolmodel nc on nlc.call_control_id = nc.id
    WHERE  (nc.call_origin = 'client' or nc.call_origin is null) and scc.slug = 'phone'
    and (DATE_FORMAT(lead.incoming_call_datetime, '%d/%m/%Y') <> DATE_FORMAT(nc.startcall, '%d/%m/%Y') or ifnull( nlc.is_duplicated, 0) = 0)
    GROUP BY lead.id, nc.id, nlc.id;


-- ########################################################################################################################


CREATE OR REPLACE VIEW
    MASTER_INFOAUTO_VIEW_OTHER_CHANNEL AS
SELECT
    lead.id,
    0 as "dd", -- Duplicado
    concessionaire.name as "Nombre de la concesion",
    o.name as "Origen",
    scc.name as "Medio",
    o2.name as "Origen publicidad",
    lead.channel2_id is not null as "Exposicion",
    concat(uu.first_name, ' ',uu.last_name) as "Asignado a",
    DATE_FORMAT(CONVERT_TZ(lead.incoming_call_datetime, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') as "Fecha llamada entrante",
    CASE
        WHEN lead.status like 'new' THEN 'Lead no atendido'
        WHEN lead.status like 'attended' THEN 'Lead atendido por comercial'
        WHEN lead.status like 'commercial_management' THEN 'Tareas pendientes'
        WHEN lead.status like 'pending' THEN 'Tareas Pendientes'
        WHEN lead.status like 'tracing' THEN 'Seguimiento'
        WHEN lead.status like 'end' THEN 'Lead cerrado'
        END as "Estado",
    CASE
        WHEN lead.result = 'not_available' then 'Descartado'
        WHEN lead.result = 'negative' then 'Descartado'
        WHEN lead.result = 'reserved_vehicle' then 'Ganado'
        WHEN lead.result = 'unreachable' then 'Descartado'
        WHEN lead.result = 'wrong' then 'Descartado'
        WHEN lead.result = 'positive' then 'Ganado'
        WHEN lead.result = 'error' then 'Descartado'
        END as "Resultado",
    lead.result_reason as "Motivo resultado",
    CASE
        WHEN lead.result = 'wrong' THEN  NULL
        WHEN client2.client_type = 'private' then 'Particular'
        WHEN client2.client_type = 'freelance' then 'Autonomo'
        WHEN client2.client_type = 'company' then 'Empresa'
        ELSE client2.client_type
        END as "Tipo cliente",
    CASE
        WHEN   lead.result = 'wrong' THEN  NULL
        ELSE client2.identification
        END as "Identificador cliente",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE client2.name
        END as "Nombre cliente",
    CASE
        WHEN   lead.result = 'wrong' THEN  NULL
        ELSE client2.business_name
        END as "Razon social cliente",
    client2.phone as "Telefono",
    client2.desk_phone as "Telefono fijo",
    client2.email as "Email",
    client2.postal_code as "Codigo postal",
    client2.address1 as "Direccion cliente",
    client2.address2 as "Direccion cliente 2",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE locality.name
        END as "Localidad",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE province.name
        END as "Provincia",
    CASE
        WHEN   lead.result = 'wrong' THEN  NULL
        ELSE v.brand_model
        END as "Vehiculo demandado Marca",
    CASE
        WHEN lead.result = 'wrong' THEN  NULL
        ELSE v.model
        END as "Vehiculo demandado Modelo",
    CASE
        WHEN   lead.result = 'wrong' THEN  NULL
        ELSE v.price
        END as "Vehiculo demandado precio",
    CASE
        WHEN   lead.result = 'wrong' THEN  NULL
        ELSE v.km
        END as "Vehiculo demandado kilometro",
    CASE
        WHEN   lead.result = 'wrong' THEN  NULL
        ELSE v.year
        END as "Vehiculo demandado anio",
    CASE
        WHEN   lead.result = 'wrong' THEN  NULL
        ELSE gastype.name
        END as "Vehiculo demandado combustible",
    CASE
        WHEN   lead.result = 'wrong' THEN  NULL
        ELSE v.vehicle_type
        END as "Vehiculo demandado tipo",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE v.comercial_category
        END as "Vehiculo demandado categoria comercial",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE v.power
        END as "Vehiculo demandado potencia",
    CASE
        WHEN   lead.result = 'wrong' THEN  NULL
        ELSE v.gear_shift
        END as "Vehiculo demandado tipo caja cambios",
    CASE
        WHEN lead.result = 'wrong' THEN  NULL
        ELSE v.ad_link
        END as "Vehiculo demandado link anuncio",
    actual_vehicle.brand as "Marca vehiculo actual",
    actual_vehicle.model as "Modelo vehiculo actual",
    actual_vehicle.version as "Version vehiculo actual",
    actual_vehicle.km as "Kilometros vehiculo actual",
    actual_vehicle.status as "Estado vehiculo actual",
    actual_vehicle.features as "Acabados vehiculo actual",
    actual_vehicle.evaluation_vo_price as "Precio evaluacion VO vehiculo actual",
    actual_vehicle.total_vehicles as "Numero vehiculos total flota",
    actual_vehicle.total_comercial_vehicles as "Numero vehiculos comerciales flota",
    actual_vehicle.total_tourism_vehicles as "Numero vehiculos turismos flota",
    actual_vehicle.fleet_notes as "Notas flota",
    actual_vehicle.license_plate as "Matricula vehiculo actual",
    DATE_FORMAT(CONVERT_TZ(actual_vehicle.buy_date, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')  as "Fecha compra vehiculo actual",
    DATE_FORMAT(CONVERT_TZ(actual_vehicle.registration_date, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')  as "Fecha matriculacion vehiculo actual",
    DATE_FORMAT(CONVERT_TZ(actual_vehicle.last_mechanic_date, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')  as "Fecha ultimo taller vehiculo actual",
    actual_vehicle.cv as "Caballos vehiculo actual",
    actual_vehicle.is_finance as "Vehiculo actual es financiado",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE GROUP_CONCAT(DISTINCT n.content
                          ORDER BY n.created ASC
                          SEPARATOR '\n')
        END as "Notas",
    CASE
        WHEN lead.result = 'wrong' THEN  NULL
        ELSE lead.score
        END as "Probabilidad de compra",
    CASE
        WHEN lead.before_reactivated_result = 'not_available' then 'No disponible'
        WHEN lead.before_reactivated_result = 'negative' then 'Descartado'
        WHEN lead.before_reactivated_result = 'reserved_vehicle' then 'Vehiculo reservado'
        WHEN lead.before_reactivated_result = 'unreachable' then 'Ilocalizable'
        WHEN lead.before_reactivated_result = 'wrong' then 'Duplicado'
        END as "Resultado historico",
    lead.is_reactivated as "Reactivado",
    DATE_FORMAT(CONVERT_TZ(lead.created, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')  as "Fecha de alta",
    1 as "LEAD RECIBIDO",
    CASE
        WHEN (lead.status='end' and lead.result_reason in ('duplicado', 'ilocalizable', 'informacion_cliente_incorrecta', 'publicidad', 'error', 'otro_departamento'))  THEN  0
        ELSE 1
        END as "LEAD UTIL",
    CASE
        WHEN (lead.result_reason not in ('duplicado', 'ilocalizable', 'informacion_cliente_incorrecta', 'publicidad', 'error', 'otro_departamento') or lead.result_reason is null)  and lead.status = 'end' THEN  1
        ELSE 0
        END as "CERRADOS",
    CASE
        WHEN (lead.result_reason not in ('duplicado', 'ilocalizable', 'informacion_cliente_incorrecta', 'publicidad', 'error', 'otro_departamento', 'vehiculo_ya_vendido') or lead.result_reason is null) and lead.status = 'end' THEN  1
        ELSE 0
        END as "DISPONIBLE",
    CASE
        WHEN (lead.result_reason is null or lead.result_reason not in ('duplicado', 'ilocalizable', 'informacion_cliente_incorrecta', 'publicidad', 'error', 'otro_departamento' 'vehiculo_ya_vendido')) and lead.status = 'end' and lead.result in ('positive', 'reserved_vehicle') THEN  1
        ELSE 0
        END  as "VENDIDO/RESERVADO",
    CASE
        WHEN (SELECT count(*) FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0) > 0 THEN true
        ELSE false
        END AS "Tareas pendientes",
    -- uu.user_activation_date as "Alta usuario",
    -- uu.user_deactivation_date as "Baja usuario"
    (select min(created) from leads_leadwhatsappmessage where lead_id=lead.id) as 'Primer Whatsapp',
    (select max(created) from leads_leadwhatsappmessage where lead_id=lead.id) as 'Ultimo Whatsapp',
    (select count(*) from leads_leadwhatsappmessage where lead_id=lead.id) as 'Numero Whatsapp',
    CASE
        WHEN   lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.outgoing_call_datetime, 'UTC', 'Europe/Madrid'),  '%d/%m/%Y %H:%i:%s')
        END as "Fecha llamada saliente",
    CASE
        WHEN lead.result = 'wrong' THEN  NULL
        WHEN lead.status_call = 'undefined' then 'Desconocido'
        WHEN lead.status_call = 'attended' then 'Atendido'
        WHEN lead.status_call = 'not_attended' then 'No atendido'
        WHEN lead.status_call = 'out_of_working_hours' then 'Fuera de horario laboral'
        END as "Status call",
    DATE_FORMAT(CONVERT_TZ(lead.incoming_email_datetime, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s') AS "Fecha email entrante", -- TODO
    DATE_FORMAT(CONVERT_TZ(lead.outgoing_email_datetime, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s') AS "Fecha email saliente", -- TODO
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.status_new_datetime, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')
        END as "Fecha lead no atendido",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.status_pending_datetime, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')
        END as "Fecha tareas pendientes",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.status_attended_datetime, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')
        END as "Fecha lead atendido",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.status_tracing_datetime, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')
        END as "Fecha lead en seguimiento",
    CASE
        WHEN lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.status_end_datetime, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')
        END as "Fecha cierre lead",
    CASE
        WHEN lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.reactivated_date, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')
        END as "Fecha reactivacion lead",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE lead.threshold_concession_call / 60
        END as "TUmbral concesion llamadas",
    CASE
        WHEN lead.result = 'wrong' THEN  NULL
        ELSE lead.threshold_concession_email / 60
        END as "TUmbral concesion email",
    CASE
        WHEN lead.result = 'wrong' THEN  NULL
        ELSE lead.computed_call_asa / 60
        END as "ASA LLAMADAS",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE lead.computed_email_asa / 60
        END as "ASA EMAIL",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        WHEN lead.computed_call_asa > lead.threshold_concession_call then 1
        WHEN lead.computed_call_asa <= lead.threshold_concession_call then 0
        END as "Tumbral llamada superado",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        WHEN lead.computed_email_asa > lead.threshold_concession_email then 1
        WHEN lead.computed_email_asa <= lead.threshold_concession_email then 0
        END as "Tumbral email superado",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(planified_realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0 ORDER BY planified_realization_date LIMIT 1
    ) AS "Fecha primera tarea programada",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(planified_realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0 ORDER BY  planified_realization_date DESC LIMIT 1
    ) AS "Fecha ultima tarea programada",
    (
        SELECT count(*) FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0
    ) as "Numero tarea programada",
    -- Tareas realizadas.
    (
        SELECT DATE_FORMAT(CONVERT_TZ(realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0  ORDER BY  realization_date DESC LIMIT 1
    ) AS "Fecha primera tarea realizada",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s')  FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0  ORDER BY  realization_date  LIMIT 1
    ) AS "Fecha ultima tarea realizada",
    (
        SELECT count(*) FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0
    ) AS "Numero de tareas programadas",
    (
        SELECT count(*) FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0 and realization_date is not null
    ) as "Numero de tareas realizadas",
    -- Seguimientos realizados
    (
        SELECT DATE_FORMAT(CONVERT_TZ(planified_realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 1 ORDER BY planified_realization_date LIMIT 1
    ) AS "Fecha primer seguimiento a programado",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(planified_realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 1 ORDER BY  planified_realization_date DESC LIMIT 1
    ) AS "Fecha ultima seguimiento a programado",
    (
        SELECT count(*) FROM leads_task WHERE lead_id=lead.id and is_traking_task = 1
    ) as "Numero seguimientos programados",
    -- Seguimientos realizados
    (
        SELECT DATE_FORMAT(CONVERT_TZ(realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 1 ORDER BY planified_realization_date LIMIT 1
    ) AS "Fecha primer seguimiento realizado",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 1 ORDER BY  planified_realization_date DESC LIMIT 1
    ) AS "Fecha ultimo seguimiento realizado",
    (
        SELECT count(*) FROM leads_task WHERE lead_id=lead.id and is_traking_task = 1 and realization_date is not null
    ) as "Numero de seguimientos realizados",
    -- Llamadas
    (
        SELECT DATE_FORMAT(CONVERT_TZ(nc.created, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM netelip_leads_callcontrolleadmodel as c
                                                                                                         INNER JOIN netelip_callcontrolmodel nc on c.call_control_id = nc.id
        WHERE c.lead_id=lead.id and nc.call_origin='user' ORDER BY nc.created
        LIMIT 1
    ) as "Fecha primera llamada cliente realizada",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(nc.created, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM netelip_leads_callcontrolleadmodel as c
                                                                                                         INNER JOIN netelip_callcontrolmodel nc on c.call_control_id = nc.id
        WHERE c.lead_id=lead.id and nc.call_origin='user' ORDER BY nc.created desc
        LIMIT 1
    ) as "Fecha ultima llamada cliente realizada",
    (
        SELECT count(*) FROM netelip_leads_callcontrolleadmodel as c
                                 INNER JOIN netelip_callcontrolmodel nc on c.call_control_id = nc.id
        WHERE c.lead_id=lead.id and nc.call_origin='user'
    ) as "Numero de llamadas realizadas",
    -- Email
    (
        SELECT DATE_FORMAT(CONVERT_TZ(created, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_leadmanagement WHERE message like '%Email enviado%' and lead_id=lead.id order by  created LIMIT 1
    ) as "Fecha primera mail enviado",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(created, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_leadmanagement WHERE message like '%Email enviado%' and lead_id=lead.id order by created desc LIMIT 1
    ) as "Fecha ultimo mail enviado",
    (
        SELECT count(*) FROM leads_leadmanagement WHERE message like '%Email enviado%' and lead_id=lead.id order by created desc
    ) as "Numero de mails enviados",
    lead.concessionaire_id,
    lead.created,
    lead.user_id
FROM leads_lead lead
             LEFT JOIN leads_concessionaire concessionaire on lead.concessionaire_id = concessionaire.id
             LEFT JOIN source_channels_source scs on lead.source_id = scs.id
             LEFT JOIN leads_origin o on scs.origin_id = o.id
             LEFT JOIN source_channels_channel scc on scs.channel_id = scc.id
             LEFT JOIN leads_origin o2 on lead.origin2_id = o2.id
             LEFT JOIN leads_client client2 on lead.client_id = client2.id
             LEFT JOIN countries_province province on client2.province_id = province.id
             LEFT JOIN countries_locality locality on client2.location_id = locality.id
             LEFT JOIN leads_vehicle v on v.lead_id = lead.id
             LEFT JOIN leads_appraisal actual_vehicle on actual_vehicle.lead_id = lead.id
             LEFT JOIN leads_gastype gastype on v.gas_id = gastype.id
             LEFT JOIN leads_lead_note lln on lead.id = lln.lead_id
             LEFT JOIN leads_note n on lln.note_id = n.id
             LEFT JOIN users_user uu on lead.user_id = uu.id
             LEFT JOIN lead_util_view lead_util on lead.id = lead_util.id
             LEFT JOIN lead_cerrados_view lead_cerrados on lead.id = lead_cerrados.id
             LEFT JOIN lead_disponible_view lead_disponible on lead.id = lead_disponible.id
             LEFT JOIN vendido_reservado_view vendido_reservado on vendido_reservado.id = lead.id
    WHERE scc.slug<>'phone'
    GROUP BY lead.id;

-- ########################################################################################################################

CREATE OR REPLACE VIEW
    MASTER_INFOAUTO_VIEW_CHANNEL_PHONE_OUTBOUND AS
SELECT
    lead.id,
    0 as "dd", -- Duplicado
    concessionaire.name as "Nombre de la concesion",
    o.name as "Origen",
    scc.name as "Medio",
    o2.name as "Origen publicidad",
    lead.channel2_id is not null as "Exposicion",
    concat(uu.first_name, ' ',uu.last_name) as "Asignado a",
    DATE_FORMAT(CONVERT_TZ(lead.incoming_call_datetime, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') as "Fecha llamada entrante",
    CASE
        WHEN lead.status like 'new' THEN 'Lead no atendido'
        WHEN lead.status like 'attended' THEN 'Lead atendido por comercial'
        WHEN lead.status like 'commercial_management' THEN 'Tareas pendientes'
        WHEN lead.status like 'pending' THEN 'Tareas Pendientes'
        WHEN lead.status like 'tracing' THEN 'Seguimiento'
        WHEN lead.status like 'end' THEN 'Lead cerrado'
        END as "Estado",
    CASE
        WHEN lead.result = 'not_available' then 'Descartado'
        WHEN lead.result = 'negative' then 'Descartado'
        WHEN lead.result = 'reserved_vehicle' then 'Ganado'
        WHEN lead.result = 'unreachable' then 'Descartado'
        WHEN lead.result = 'wrong' then 'Descartado'
        WHEN lead.result = 'positive' then 'Ganado'
        WHEN lead.result = 'error' then 'Descartado'
        END as "Resultado",
    lead.result_reason as "Motivo resultado",
    CASE
        WHEN lead.result = 'wrong' THEN  NULL
        WHEN client2.client_type = 'private' then 'Particular'
        WHEN client2.client_type = 'freelance' then 'Autonomo'
        WHEN client2.client_type = 'company' then 'Empresa'
        ELSE client2.client_type
        END as "Tipo cliente",
    CASE
        WHEN   lead.result = 'wrong' THEN  NULL
        ELSE client2.identification
        END as "Identificador cliente",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE client2.name
        END as "Nombre cliente",
    CASE
        WHEN   lead.result = 'wrong' THEN  NULL
        ELSE client2.business_name
        END as "Razon social cliente",
    client2.phone as "Telefono",
    client2.desk_phone as "Telefono fijo",
    client2.email as "Email",
    client2.postal_code as "Codigo postal",
    client2.address1 as "Direccion cliente",
    client2.address2 as "Direccion cliente 2",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE locality.name
        END as "Localidad",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE province.name
        END as "Provincia",
    CASE
        WHEN   lead.result = 'wrong' THEN  NULL
        ELSE v.brand_model
        END as "Vehiculo demandado Marca",
    CASE
        WHEN lead.result = 'wrong' THEN  NULL
        ELSE v.model
        END as "Vehiculo demandado Modelo",
    CASE
        WHEN   lead.result = 'wrong' THEN  NULL
        ELSE v.price
        END as "Vehiculo demandado precio",
    CASE
        WHEN   lead.result = 'wrong' THEN  NULL
        ELSE v.km
        END as "Vehiculo demandado kilometro",
    CASE
        WHEN   lead.result = 'wrong' THEN  NULL
        ELSE v.year
        END as "Vehiculo demandado anio",
    CASE
        WHEN   lead.result = 'wrong' THEN  NULL
        ELSE gastype.name
        END as "Vehiculo demandado combustible",
    CASE
        WHEN   lead.result = 'wrong' THEN  NULL
        ELSE v.vehicle_type
        END as "Vehiculo demandado tipo",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE v.comercial_category
        END as "Vehiculo demandado categoria comercial",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE v.power
        END as "Vehiculo demandado potencia",
    CASE
        WHEN   lead.result = 'wrong' THEN  NULL
        ELSE v.gear_shift
        END as "Vehiculo demandado tipo caja cambios",
    CASE
        WHEN lead.result = 'wrong' THEN  NULL
        ELSE v.ad_link
        END as "Vehiculo demandado link anuncio",
    actual_vehicle.brand as "Marca vehiculo actual",
    actual_vehicle.model as "Modelo vehiculo actual",
    actual_vehicle.version as "Version vehiculo actual",
    actual_vehicle.km as "Kilometros vehiculo actual",
    actual_vehicle.status as "Estado vehiculo actual",
    actual_vehicle.features as "Acabados vehiculo actual",
    actual_vehicle.evaluation_vo_price as "Precio evaluacion VO vehiculo actual",
    actual_vehicle.total_vehicles as "Numero vehiculos total flota",
    actual_vehicle.total_comercial_vehicles as "Numero vehiculos comerciales flota",
    actual_vehicle.total_tourism_vehicles as "Numero vehiculos turismos flota",
    actual_vehicle.fleet_notes as "Notas flota",
    actual_vehicle.license_plate as "Matricula vehiculo actual",
    DATE_FORMAT(CONVERT_TZ(actual_vehicle.buy_date, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')  as "Fecha compra vehiculo actual",
    DATE_FORMAT(CONVERT_TZ(actual_vehicle.registration_date, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')  as "Fecha matriculacion vehiculo actual",
    DATE_FORMAT(CONVERT_TZ(actual_vehicle.last_mechanic_date, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')  as "Fecha ultimo taller vehiculo actual",
    actual_vehicle.cv as "Caballos vehiculo actual",
    actual_vehicle.is_finance as "Vehiculo actual es financiado",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE GROUP_CONCAT(DISTINCT n.content
                          ORDER BY n.created ASC
                          SEPARATOR '\n')
        END as "Notas",
    CASE
        WHEN lead.result = 'wrong' THEN  NULL
        ELSE lead.score
        END as "Probabilidad de compra",
    CASE
        WHEN lead.before_reactivated_result = 'not_available' then 'No disponible'
        WHEN lead.before_reactivated_result = 'negative' then 'Descartado'
        WHEN lead.before_reactivated_result = 'reserved_vehicle' then 'Vehiculo reservado'
        WHEN lead.before_reactivated_result = 'unreachable' then 'Ilocalizable'
        WHEN lead.before_reactivated_result = 'wrong' then 'Duplicado'
        END as "Resultado historico",
    lead.is_reactivated as "Reactivado",
    DATE_FORMAT(CONVERT_TZ(lead.created, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')  as "Fecha de alta",
    1 as "LEAD RECIBIDO",
    CASE
        WHEN (lead.status='end' and lead.result_reason in ('duplicado', 'ilocalizable', 'informacion_cliente_incorrecta', 'publicidad', 'error', 'otro_departamento'))  THEN  0
        ELSE 1
        END as "LEAD UTIL",
    CASE
        WHEN (lead.result_reason not in ('duplicado', 'ilocalizable', 'informacion_cliente_incorrecta', 'publicidad', 'error', 'otro_departamento') or lead.result_reason is null) and lead.status = 'end' THEN  1
        ELSE 0
        END as "CERRADOS",
    CASE
        WHEN (lead.result_reason not in ('duplicado', 'ilocalizable', 'informacion_cliente_incorrecta', 'publicidad', 'error', 'otro_departamento', 'vehiculo_ya_vendido') or lead.result_reason is null) and lead.status = 'end' THEN  1
        ELSE 0
        END as "DISPONIBLE",
    CASE
        WHEN (lead.result_reason is null or lead.result_reason not in ('duplicado', 'ilocalizable', 'informacion_cliente_incorrecta', 'publicidad', 'error', 'otro_departamento' 'vehiculo_ya_vendido')) and lead.status = 'end' and lead.result in ('positive', 'reserved_vehicle') THEN  1
        ELSE 0
        END  as "VENDIDO/RESERVADO",
    CASE
        WHEN (SELECT count(*) FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0) > 0 THEN true
        ELSE false
        END AS "Tareas pendientes",
    -- uu.user_activation_date as "Alta usuario",
    -- uu.user_deactivation_date as "Baja usuario"
    (select min(created) from leads_leadwhatsappmessage where lead_id=lead.id) as 'Primer Whatsapp',
    (select max(created) from leads_leadwhatsappmessage where lead_id=lead.id) as 'Ultimo Whatsapp',
    (select count(*) from leads_leadwhatsappmessage where lead_id=lead.id) as 'Numero Whatsapp',
    CASE
        WHEN   lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.outgoing_call_datetime, 'UTC', 'Europe/Madrid'),  '%d/%m/%Y %H:%i:%s')
        END as "Fecha llamada saliente",
    CASE
        WHEN lead.result = 'wrong' THEN  NULL
        WHEN lead.status_call = 'undefined' then 'Desconocido'
        WHEN lead.status_call = 'attended' then 'Atendido'
        WHEN lead.status_call = 'not_attended' then 'No atendido'
        WHEN lead.status_call = 'out_of_working_hours' then 'Fuera de horario laboral'
        END as "Status call",
    DATE_FORMAT(CONVERT_TZ(lead.incoming_email_datetime, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s') AS "Fecha email entrante", -- TODO
    DATE_FORMAT(lead.outgoing_email_datetime,'%d/%m/%Y %H:%i:%s') AS "Fecha email saliente", -- TODO
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.status_new_datetime, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')
        END as "Fecha lead no atendido",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.status_pending_datetime, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')
        END as "Fecha tareas pendientes",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.status_attended_datetime, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')
        END as "Fecha lead atendido",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.status_tracing_datetime, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')
        END as "Fecha lead en seguimiento",
    CASE
        WHEN lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.status_end_datetime, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')
        END as "Fecha cierre lead",
    CASE
        WHEN lead.result = 'wrong' THEN  NULL
        ELSE DATE_FORMAT(CONVERT_TZ(lead.reactivated_date, 'UTC', 'Europe/Madrid'),'%d/%m/%Y %H:%i:%s')
        END as "Fecha reactivacion lead",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE lead.threshold_concession_call / 60
        END as "TUmbral concesion llamadas",
    CASE
        WHEN lead.result = 'wrong' THEN  NULL
        ELSE lead.threshold_concession_email / 60
        END as "TUmbral concesion email",
    CASE
        WHEN lead.result = 'wrong' THEN  NULL
        ELSE lead.computed_call_asa / 60
        END as "ASA LLAMADAS",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        ELSE lead.computed_email_asa / 60
        END as "ASA EMAIL",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        WHEN lead.computed_call_asa > lead.threshold_concession_call then 1
        WHEN lead.computed_call_asa <= lead.threshold_concession_call then 0
        END as "Tumbral llamada superado",
    CASE
        WHEN  lead.result = 'wrong' THEN  NULL
        WHEN lead.computed_email_asa > lead.threshold_concession_email then 1
        WHEN lead.computed_email_asa <= lead.threshold_concession_email then 0
        END as "Tumbral email superado",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(planified_realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0 ORDER BY planified_realization_date LIMIT 1
    ) AS "Fecha primera tarea programada",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(planified_realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0 ORDER BY  planified_realization_date DESC LIMIT 1
    ) AS "Fecha ultima tarea programada",
    (
        SELECT count(*) FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0
    ) as "Numero tarea programada",
    -- Tareas realizadas.
    (
        SELECT DATE_FORMAT(CONVERT_TZ(realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0  ORDER BY  realization_date DESC LIMIT 1
    ) AS "Fecha primera tarea realizada",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s')  FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0  ORDER BY  realization_date  LIMIT 1
    ) AS "Fecha ultima tarea realizada",
    (
        SELECT count(*) FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0
    ) AS "Numero de tareas programadas",
    (
        SELECT count(*) FROM leads_task WHERE lead_id=lead.id and is_traking_task = 0 and realization_date is not null
    ) as "Numero de tareas realizadas",
    -- Seguimientos realizados
    (
        SELECT DATE_FORMAT(CONVERT_TZ(planified_realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 1 ORDER BY planified_realization_date LIMIT 1
    ) AS "Fecha primer seguimiento a programado",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(planified_realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 1 ORDER BY  planified_realization_date DESC LIMIT 1
    ) AS "Fecha ultima seguimiento a programado",
    (
        SELECT count(*) FROM leads_task WHERE lead_id=lead.id and is_traking_task = 1
    ) as "Numero seguimientos programados",
    -- Seguimientos realizados
    (
        SELECT DATE_FORMAT(CONVERT_TZ(realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 1 ORDER BY planified_realization_date LIMIT 1
    ) AS "Fecha primer seguimiento realizado",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(realization_date, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_task WHERE lead_id=lead.id and is_traking_task = 1 ORDER BY  planified_realization_date DESC LIMIT 1
    ) AS "Fecha ultimo seguimiento realizado",
    (
        SELECT count(*) FROM leads_task WHERE lead_id=lead.id and is_traking_task = 1 and realization_date is not null
    ) as "Numero de seguimientos realizados",
    -- Llamadas
    (
        SELECT DATE_FORMAT(CONVERT_TZ(nc.created, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM netelip_leads_callcontrolleadmodel as c
                                                                                                         INNER JOIN netelip_callcontrolmodel nc on c.call_control_id = nc.id
        WHERE c.lead_id=lead.id and nc.call_origin='user' ORDER BY nc.created
        LIMIT 1
    ) as "Fecha primera llamada cliente realizada",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(nc.created, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM netelip_leads_callcontrolleadmodel as c
                                                                                                         INNER JOIN netelip_callcontrolmodel nc on c.call_control_id = nc.id
        WHERE c.lead_id=lead.id and nc.call_origin='user' ORDER BY nc.created desc
        LIMIT 1
    ) as "Fecha ultima llamada cliente realizada",
    (
        SELECT count(*) FROM netelip_leads_callcontrolleadmodel as c
                                 INNER JOIN netelip_callcontrolmodel nc on c.call_control_id = nc.id
        WHERE c.lead_id=lead.id and nc.call_origin='user'
    ) as "Numero de llamadas realizadas",
    -- Email
    (
        SELECT DATE_FORMAT(CONVERT_TZ(created, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_leadmanagement WHERE message like '%Email enviado%' and lead_id=lead.id order by  created LIMIT 1
    ) as "Fecha primera mail enviado",
    (
        SELECT DATE_FORMAT(CONVERT_TZ(created, 'UTC', 'Europe/Madrid'), '%d/%m/%Y %H:%i:%s') FROM leads_leadmanagement WHERE message like '%Email enviado%' and lead_id=lead.id order by created desc LIMIT 1
    ) as "Fecha ultimo mail enviado",
    (
        SELECT count(*) FROM leads_leadmanagement WHERE message like '%Email enviado%' and lead_id=lead.id order by created desc
    ) as "Numero de mails enviados",
    lead.concessionaire_id,
    lead.created,
    lead.user_id
FROM leads_lead lead
             LEFT JOIN leads_concessionaire concessionaire on lead.concessionaire_id = concessionaire.id
                       LEFT JOIN source_channels_source scs on lead.source_id = scs.id
                       LEFT JOIN leads_origin o on scs.origin_id = o.id
                       LEFT JOIN source_channels_channel scc on scs.channel_id = scc.id
                       LEFT JOIN leads_origin o2 on lead.origin2_id = o2.id
                       LEFT JOIN leads_client client2 on lead.client_id = client2.id
                       LEFT JOIN countries_province province on client2.province_id = province.id
                       LEFT JOIN countries_locality locality on client2.location_id = locality.id
                       LEFT JOIN leads_vehicle v on v.lead_id = lead.id
                       LEFT JOIN leads_appraisal actual_vehicle on actual_vehicle.lead_id = lead.id
                       LEFT JOIN leads_gastype gastype on v.gas_id = gastype.id
                       LEFT JOIN leads_lead_note lln on lead.id = lln.lead_id
                       LEFT JOIN leads_note n on lln.note_id = n.id
                       LEFT JOIN users_user uu on lead.user_id = uu.id
                       LEFT JOIN lead_util_view lead_util on lead.id = lead_util.id
                       LEFT JOIN lead_cerrados_view lead_cerrados on lead.id = lead_cerrados.id
                       LEFT JOIN lead_disponible_view lead_disponible on lead.id = lead_disponible.id
                       LEFT JOIN vendido_reservado_view vendido_reservado on vendido_reservado.id = lead.id
                   WHERE lead.id not in (select id from MASTER_INFOAUTO_VIEW_CHANNEL_PHONE where dd=0) and lead.id not in (select id from MASTER_INFOAUTO_VIEW_OTHER_CHANNEL)
                   GROUP BY lead.id;

-- ########################################################################################################################

CREATE OR REPLACE VIEW
    MASTER_INFOAUTO_VIEW AS
SELECT * FROM  (
                   (SELECT * FROM MASTER_INFOAUTO_VIEW_CHANNEL_PHONE where (dd=0) and (Resultado not like 'Ilocalizable' or Resultado is null)) UNION ALL
                   (SELECT * FROM MASTER_INFOAUTO_VIEW_OTHER_CHANNEL where (dd=0) and (Resultado not like 'Ilocalizable' or Resultado is null)) UNION ALL
                   (SELECT * FROM MASTER_INFOAUTO_VIEW_CHANNEL_PHONE_OUTBOUND where (dd=0) and (Resultado not like 'Ilocalizable' or Resultado is null))
               ) as final;


-- # Para comprobar maestro.
-- SELECT (SELECT COUNT(*) FROM MASTER_INFOAUTO_VIEW where dd=0) = (SELECT COUNT(*) FROM leads_lead) as compare; .
-- SELECT * FROM MASTER_INFOAUTO_VIEW
