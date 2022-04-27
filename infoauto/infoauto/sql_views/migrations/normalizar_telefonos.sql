update leads_client set phone = concat('+34', phone) where length(phone) = 9;
update leads_client set phone = concat('+',substr(phone, 3)) where phone like '00%' ;
update leads_client set phone = concat('+',phone) where phone not like '\+%' and phone not like '';

update leads_client set desk_phone = concat('+34', desk_phone) where length(desk_phone) = 9;
update leads_client set desk_phone = concat('+',substr(desk_phone, 3)) where desk_phone like '00%' ;
update leads_client set desk_phone = concat('+',desk_phone) where desk_phone not like '\+%' and desk_phone not like '';

update source_channels_source set `data` = concat('+34', `data`) where length(`data`) = 9 and channel_id=1;
update source_channels_source set `data` = concat('+',substr(`data`, 3)) where `data` like '00%' and channel_id=1;
update source_channels_source set `data` = concat('+',`data`) where `data` not like '\+%' and `data` not like '' and channel_id=1;

update leads_phone set `number` = concat('+34', `number`) where length(`number`) = 9;
update leads_phone set `number` = concat('+',substr(`number`, 3)) where `number` like '00%' ;
update leads_phone set `number` = concat('+',`number`) where `number` not like '\+%' and `number` not like '';

update leads_lead set concession_phone = concat('+34', concession_phone) where length(concession_phone) = 9;
update leads_lead set concession_phone = concat('+',substr(concession_phone, 3)) where concession_phone like '00%' ;
update leads_lead set concession_phone = concat('+',concession_phone) where concession_phone not like '\+%' and concession_phone not like '';

update leads_concessionaire set concession_phone = concat('+34', concession_phone) where length(concession_phone) = 9;
update leads_concessionaire set concession_phone = concat('+',substr(concession_phone, 3)) where concession_phone like '00%' ;
update leads_concessionaire set concession_phone = concat('+',concession_phone) where concession_phone not like '\+%' and concession_phone not like '';

update leads_concessionaire set mask_c2c = concat('+34', mask_c2c) where length(mask_c2c) = 9;
update leads_concessionaire set mask_c2c = concat('+',substr(mask_c2c, 3)) where mask_c2c like '00%' ;
update leads_concessionaire set mask_c2c = concat('+',mask_c2c) where mask_c2c not like '\+%' and mask_c2c not like '';

update netelip_callcontrolmodel set src = concat('+34', src) where length(src) = 9;
update netelip_callcontrolmodel set src = concat('+',substr(src, 3)) where src like '00%' ;
update netelip_callcontrolmodel set src = concat('+',src) where src not like '\+%' and src;

update netelip_callcontrolmodel set dst = concat('+34', dst) where length(dst) = 9;
update netelip_callcontrolmodel set dst = concat('+',substr(dst, 3)) where dst like '00%' ;
update netelip_callcontrolmodel set dst = concat('+',dst) where dst not like '\+%' and dst not like '';

