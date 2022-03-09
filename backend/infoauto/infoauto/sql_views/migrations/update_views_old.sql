CREATE OR REPLACE VIEW
     MASTER_INFOAUTO_VIEW_CHANNEL_PHONE AS
SELECT
        lead.id,
        ifnull( nlc.is_duplicated, 0) as "duplicado",
        concessionaire.name as "Nombre de la concesion",
        o.name as "Origen",
        scc.name as "Medio",
       concat(uu.first_name, ' ',uu.last_name) as "Asignado a",
       DATE_FORMAT(lead.incoming_call_datetime, '%d/%m/%Y %H:%i:%s') as "Fecha llamada entrante",
        CASE
            WHEN nlc.is_duplicated = 1 THEN 'Finalizado'
            WHEN lead.status like 'new' THEN 'Lead no atendido'
            WHEN lead.status like 'attended' THEN 'Lead atendido'
            WHEN lead.status like 'commercial_management' THEN 'Gestion comercial'
            WHEN lead.status like 'pending' THEN 'Tareas Pendientes'
            WHEN lead.status like 'tracing' THEN 'Seguimiento'
            WHEN lead.status like 'end' THEN 'Cerrado'
        END as "Estado",
        CASE
            WHEN nlc.is_duplicated = 1 THEN 'Duplicado'
            WHEN lead.result = 'not_available' then 'No disponible'
            WHEN lead.result = 'negative' then 'Negativo'
            WHEN lead.result = 'reserved_vehicle' then 'Vehiculo reservado'
            WHEN lead.result = 'unreachable' then 'Ilocalizable'
            WHEN lead.result = 'wrong' then 'Duplicado'
            WHEN lead.result = 'positive' then 'Ganado'
            WHEN lead.result = 'error' then 'Error'
        END as "Resultado",
        lead.result_reason as "Motivo resultado",
        CASE
            WHEN lead.result = 'positive' or lead.result = 'reserved_vehicle' then TRUE
            ELSE FALSE
        END  as "VENDIDO/RESERVADO",
        CASE
            WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
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
        END as "Vehiculo demandada modelo marca",
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
        DATE_FORMAT(actual_vehicle.buy_date,'%d/%m/%Y %H:%i:%s')  as "Fecha compra vehiculo actual",
        DATE_FORMAT(actual_vehicle.registration_date,'%d/%m/%Y %H:%i:%s')  as "Fecha matriculacion vehiculo actual",
        DATE_FORMAT(actual_vehicle.last_mechanic_date,'%d/%m/%Y %H:%i:%s')  as "Fecha ultimo taller vehiculo actual",
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
            WHEN lead.before_reactivated_result = 'negative' then 'Negativo'
            WHEN lead.before_reactivated_result = 'reserved_vehicle' then 'Vehiculo reservado'
            WHEN lead.before_reactivated_result = 'unreachable' then 'Ilocalizable'
            WHEN lead.before_reactivated_result = 'wrong' then 'Duplicado'
        END as "Resultado historico",
        lead.is_reactivated as "Reactivado",
        true as "LEAD RECIBIDO",
        DATE_FORMAT(lead.created,'%d/%m/%Y %H:%i:%s')  as "Fecha de alta",
        CASE
            WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
            ELSE lead_util.lead_util
        END as "LEAD UTIL",
        CASE
            WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
            ELSE lead_cerrados.lead_cerrados
        END as "CERRADOS",
        CASE
            WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
            ELSE lead_disponible.lead_disponible
        END as "Disponible",
        CASE
            WHEN lead.status like 'pending' or lead.status like 'commercial_management' THEN true
            ELSE false
        END AS "Tareas pendientes",
        -- uu.user_activation_date as "Alta usuario",
        -- uu.user_deactivation_date as "Baja usuario"
        CASE
            WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.outgoing_call_datetime,  '%d/%m/%Y %H:%i:%s')
        END as "Fecha llamada saliente",
        CASE
            WHEN nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
            WHEN lead.status_call = 'undefined' then 'Desconocido'
            WHEN lead.status_call = 'attended' then 'Atendido'
            WHEN lead.status_call = 'not_attended' then 'No atendido'
            WHEN lead.status_call = 'out_of_working_hours' then 'Fuera de horario laboral'
        END as "Status call",
        DATE_FORMAT(lead.incoming_email_datetime,'%d/%m/%Y %H:%i:%s') AS "Fecha email entrante", -- TODO
        DATE_FORMAT(lead.outgoing_email_datetime,'%d/%m/%Y %H:%i:%s') AS "Fecha email saliente", -- TODO
        CASE
            WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.status_new_datetime,'%d/%m/%Y %H:%i:%s')
        END as "Fecha lead no atendido",
        CASE
            WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.status_pending_datetime,'%d/%m/%Y %H:%i:%s')
        END as "Fecha tareas pendientes",
        CASE
            WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.status_attended_datetime,'%d/%m/%Y %H:%i:%s')
        END as "Fecha lead atendido",
        CASE
            WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.status_tracing_datetime,'%d/%m/%Y %H:%i:%s')
        END as "Fecha lead en seguimiento",
        CASE
            WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.status_end_datetime,'%d/%m/%Y %H:%i:%s')
        END as "Fecha cierre lead",
        CASE
            WHEN  nlc.is_duplicated = 1 or lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.reactivated_date,'%d/%m/%Y %H:%i:%s')
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
        ifnull( nlc.is_duplicated, 0) AS "Lead es duplicado",
        nc.id AS "Identificador interno llamada",
        nc.id_call AS "Identificador netelip de llamada",
    lead.concessionaire_id,
    lead.created,
    lead.user_id
    FROM leads_lead lead
             LEFT JOIN leads_concessionaire concessionaire on lead.concessionaire_id = concessionaire.id
             LEFT JOIN source_channels_source scs on lead.source_id = scs.id
             LEFT JOIN leads_origin o on scs.origin_id = o.id
             LEFT JOIN source_channels_channel scc on scs.channel_id = scc.id
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
        0 as "duplicado",
        concessionaire.name as "Nombre de la concesion",
        o.name as "Origen",
        scc.name as "Medio",
       concat(uu.first_name, ' ',uu.last_name) as "Asignado a",
       DATE_FORMAT(lead.incoming_call_datetime, '%d/%m/%Y %H:%i:%s') as "Fecha llamada entrante",
        CASE
            WHEN lead.status like 'new' THEN 'Lead no atendido'
            WHEN lead.status like 'attended' THEN 'Lead atendido'
            WHEN lead.status like 'commercial_management' THEN 'Gestion comercial'
            WHEN lead.status like 'pending' THEN 'Tareas Pendientes'
            WHEN lead.status like 'tracing' THEN 'Seguimiento'
            WHEN lead.status like 'end' THEN 'Cerrado'
        END as "Estado",
        CASE
            WHEN lead.result = 'not_available' then 'No disponible'
            WHEN lead.result = 'negative' then 'Negativo'
            WHEN lead.result = 'reserved_vehicle' then 'Vehiculo reservado'
            WHEN lead.result = 'unreachable' then 'Ilocalizable'
            WHEN lead.result = 'wrong' then 'Duplicado'
            WHEN lead.result = 'positive' then 'Ganado'
            WHEN lead.result = 'error' then 'Error'
        END as "Resultado",
        lead.result_reason as "Motivo resultado",
        CASE
            WHEN lead.result = 'positive'  or lead.result = 'reserved_vehicle' then TRUE
            ELSE FALSE
        END  as "VENDIDO/RESERVADO",
        CASE
            WHEN   lead.result = 'wrong' THEN  NULL
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
        END as "Vehiculo demandada modelo marca",
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
        DATE_FORMAT(actual_vehicle.buy_date,'%d/%m/%Y %H:%i:%s')  as "Fecha compra vehiculo actual",
        DATE_FORMAT(actual_vehicle.registration_date,'%d/%m/%Y %H:%i:%s')  as "Fecha matriculacion vehiculo actual",
        DATE_FORMAT(actual_vehicle.last_mechanic_date,'%d/%m/%Y %H:%i:%s')  as "Fecha ultimo taller vehiculo actual",
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
            WHEN lead.before_reactivated_result = 'negative' then 'Negativo'
            WHEN lead.before_reactivated_result = 'reserved_vehicle' then 'Vehiculo reservado'
            WHEN lead.before_reactivated_result = 'unreachable' then 'Ilocalizable'
            WHEN lead.before_reactivated_result = 'wrong' then 'Duplicado'
        END as "Resultado historico",
        lead.is_reactivated as "Reactivado",
        true as "LEAD RECIBIDO",
        DATE_FORMAT(lead.created,'%d/%m/%Y %H:%i:%s')  as "Fecha de alta",
        CASE
            WHEN  lead.result = 'wrong' THEN  NULL
            ELSE lead_util.lead_util
        END as "LEAD UTIL",
        CASE
            WHEN  lead.result = 'wrong' THEN  NULL
            ELSE lead_cerrados.lead_cerrados
        END as "CERRADOS",
        CASE
            WHEN  lead.result = 'wrong' THEN  NULL
            ELSE lead_disponible.lead_disponible
        END as "Disponible",
        CASE
            WHEN lead.status like 'pending' or lead.status like 'commercial_management' THEN true
            ELSE false
        END AS "Tareas pendientes",
        -- uu.user_activation_date as "Alta usuario",
        -- uu.user_deactivation_date as "Baja usuario"
        CASE
            WHEN   lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.outgoing_call_datetime,  '%d/%m/%Y %H:%i:%s')
        END as "Fecha llamada saliente",
        CASE
            WHEN lead.result = 'wrong' THEN  NULL
            WHEN lead.status_call = 'undefined' then 'Desconocido'
            WHEN lead.status_call = 'attended' then 'Atendido'
            WHEN lead.status_call = 'not_attended' then 'No atendido'
            WHEN lead.status_call = 'out_of_working_hours' then 'Fuera de horario laboral'
        END as "Status call",
        DATE_FORMAT(lead.incoming_email_datetime,'%d/%m/%Y %H:%i:%s') AS "Fecha email entrante", -- TODO
        DATE_FORMAT(lead.outgoing_email_datetime,'%d/%m/%Y %H:%i:%s') AS "Fecha email saliente", -- TODO
        CASE
            WHEN  lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.status_new_datetime,'%d/%m/%Y %H:%i:%s')
        END as "Fecha lead no atendido",
        CASE
            WHEN  lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.status_pending_datetime,'%d/%m/%Y %H:%i:%s')
        END as "Fecha tareas pendientes",
        CASE
            WHEN  lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.status_attended_datetime,'%d/%m/%Y %H:%i:%s')
        END as "Fecha lead atendido",
        CASE
            WHEN  lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.status_tracing_datetime,'%d/%m/%Y %H:%i:%s')
        END as "Fecha lead en seguimiento",
        CASE
            WHEN lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.status_end_datetime,'%d/%m/%Y %H:%i:%s')
        END as "Fecha cierre lead",
        CASE
            WHEN lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.reactivated_date,'%d/%m/%Y %H:%i:%s')
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
        0 AS "Lead es duplicado",
        NULL AS "Identificador interno llamada",
        NULL AS "Identificador netelip de llamada",
    lead.concessionaire_id,
    lead.created,
    lead.user_id
    FROM leads_lead lead
             LEFT JOIN leads_concessionaire concessionaire on lead.concessionaire_id = concessionaire.id
             LEFT JOIN source_channels_source scs on lead.source_id = scs.id
             LEFT JOIN leads_origin o on scs.origin_id = o.id
             LEFT JOIN source_channels_channel scc on scs.channel_id = scc.id
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
        0 as "duplicado",
        concessionaire.name as "Nombre de la concesion",
        o.name as "Origen",
        scc.name as "Medio",
       concat(uu.first_name, ' ',uu.last_name) as "Asignado a",
       DATE_FORMAT(lead.incoming_call_datetime, '%d/%m/%Y %H:%i:%s') as "Fecha llamada entrante",
        CASE
            WHEN lead.status like 'new' THEN 'Lead no atendido'
            WHEN lead.status like 'attended' THEN 'Lead atendido'
            WHEN lead.status like 'commercial_management' THEN 'Gestion comercial'
            WHEN lead.status like 'pending' THEN 'Tareas Pendientes'
            WHEN lead.status like 'tracing' THEN 'Seguimiento'
            WHEN lead.status like 'end' THEN 'Cerrado'
        END as "Estado",
        CASE
            WHEN lead.result = 'not_available' then 'No disponible'
            WHEN lead.result = 'negative' then 'Negativo'
            WHEN lead.result = 'reserved_vehicle' then 'Vehiculo reservado'
            WHEN lead.result = 'unreachable' then 'Ilocalizable'
            WHEN lead.result = 'wrong' then 'Duplicado'
            WHEN lead.result = 'positive' then 'Ganado'
            WHEN lead.result = 'error' then 'Error'
        END as "Resultado",
        lead.result_reason as "Motivo resultado",
        CASE
            WHEN lead.result = 'positive'  or lead.result = 'reserved_vehicle'  then TRUE
            ELSE FALSE
        END  as "VENDIDO/RESERVADO",
        CASE
            WHEN   lead.result = 'wrong' THEN  NULL
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
        END as "Vehiculo demandada modelo marca",
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
        DATE_FORMAT(actual_vehicle.buy_date,'%d/%m/%Y %H:%i:%s')  as "Fecha compra vehiculo actual",
        DATE_FORMAT(actual_vehicle.registration_date,'%d/%m/%Y %H:%i:%s')  as "Fecha matriculacion vehiculo actual",
        DATE_FORMAT(actual_vehicle.last_mechanic_date,'%d/%m/%Y %H:%i:%s')  as "Fecha ultimo taller vehiculo actual",
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
            WHEN lead.before_reactivated_result = 'negative' then 'Negativo'
            WHEN lead.before_reactivated_result = 'reserved_vehicle' then 'Vehiculo reservado'
            WHEN lead.before_reactivated_result = 'unreachable' then 'Ilocalizable'
            WHEN lead.before_reactivated_result = 'wrong' then 'Duplicado'
        END as "Resultado historico",
        lead.is_reactivated as "Reactivado",
        true as "LEAD RECIBIDO",
        DATE_FORMAT(lead.created,'%d/%m/%Y %H:%i:%s')  as "Fecha de alta",
        CASE
            WHEN  lead.result = 'wrong' THEN  NULL
            ELSE lead_util.lead_util
        END as "LEAD UTIL",
        CASE
            WHEN  lead.result = 'wrong' THEN  NULL
            ELSE lead_cerrados.lead_cerrados
        END as "CERRADOS",
        CASE
            WHEN  lead.result = 'wrong' THEN  NULL
            ELSE lead_disponible.lead_disponible
        END as "Disponible",
        CASE
            WHEN lead.status like 'pending' or lead.status like 'commercial_management' THEN true
            ELSE false
        END AS "Tareas pendientes",
        -- uu.user_activation_date as "Alta usuario",
        -- uu.user_deactivation_date as "Baja usuario"
        CASE
            WHEN   lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.outgoing_call_datetime,  '%d/%m/%Y %H:%i:%s')
        END as "Fecha llamada saliente",
        CASE
            WHEN lead.result = 'wrong' THEN  NULL
            WHEN lead.status_call = 'undefined' then 'Desconocido'
            WHEN lead.status_call = 'attended' then 'Atendido'
            WHEN lead.status_call = 'not_attended' then 'No atendido'
            WHEN lead.status_call = 'out_of_working_hours' then 'Fuera de horario laboral'
        END as "Status call",
        DATE_FORMAT(lead.incoming_email_datetime,'%d/%m/%Y %H:%i:%s') AS "Fecha email entrante", -- TODO
        DATE_FORMAT(lead.outgoing_email_datetime,'%d/%m/%Y %H:%i:%s') AS "Fecha email saliente", -- TODO
        CASE
            WHEN  lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.status_new_datetime,'%d/%m/%Y %H:%i:%s')
        END as "Fecha lead no atendido",
        CASE
            WHEN  lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.status_pending_datetime,'%d/%m/%Y %H:%i:%s')
        END as "Fecha tareas pendientes",
        CASE
            WHEN  lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.status_attended_datetime,'%d/%m/%Y %H:%i:%s')
        END as "Fecha lead atendido",
        CASE
            WHEN  lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.status_tracing_datetime,'%d/%m/%Y %H:%i:%s')
        END as "Fecha lead en seguimiento",
        CASE
            WHEN lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.status_end_datetime,'%d/%m/%Y %H:%i:%s')
        END as "Fecha cierre lead",
        CASE
            WHEN lead.result = 'wrong' THEN  NULL
            ELSE DATE_FORMAT(lead.reactivated_date,'%d/%m/%Y %H:%i:%s')
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
        0 AS "Lead es duplicado",
        NULL AS "Identificador interno llamada",
        NULL AS "Identificador netelip de llamada",
    lead.concessionaire_id,
    lead.created,
    lead.user_id
    FROM leads_lead lead
             LEFT JOIN leads_concessionaire concessionaire on lead.concessionaire_id = concessionaire.id
             LEFT JOIN source_channels_source scs on lead.source_id = scs.id
             LEFT JOIN leads_origin o on scs.origin_id = o.id
             LEFT JOIN source_channels_channel scc on scs.channel_id = scc.id
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
    WHERE lead.id not in (select id from MASTER_INFOAUTO_VIEW_CHANNEL_PHONE where duplicado=0) and lead.id not in (select id from MASTER_INFOAUTO_VIEW_OTHER_CHANNEL)
    GROUP BY lead.id;

-- ########################################################################################################################

CREATE OR REPLACE VIEW
    MASTER_INFOAUTO_VIEW AS
    SELECT * FROM  (
        (SELECT * FROM MASTER_INFOAUTO_VIEW_CHANNEL_PHONE) UNION ALL
        (SELECT * FROM MASTER_INFOAUTO_VIEW_OTHER_CHANNEL) UNION ALL
        (SELECT * FROM MASTER_INFOAUTO_VIEW_CHANNEL_PHONE_OUTBOUND)
) as final;

-- # Para comprobar maestro.
-- SELECT (SELECT COUNT(*) FROM MASTER_INFOAUTO_VIEW where duplicado=0) = (SELECT COUNT(*) FROM leads_lead) as compare; .
